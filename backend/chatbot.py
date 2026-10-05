#!usr/env/bin python3
import os
import redis
import json

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import  RunnablePassthrough ,  RunnableLambda , RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import messages_from_dict, messages_to_dict , HumanMessage, AIMessage

from operator import itemgetter

# help(HuggingFaceEndpointEmbeddings)

# === INITIALIZATION ===
model_name    = "sentence-transformers/all-MiniLM-L6-v2" # name of the model to use from huggingface
model_kwargs  = {"device":"cpu"}
encode_kwargs = {"normalize_embeddings": True}

# Loading the API key
load_dotenv()

if not os.getenv("GROQ_API_KEY") or not os.getenv("HF_TOKEN") or not os.getenv("REDIS_URL"):
    raise ValueError(" API KEYS NOT FOUND !!!")

# Loading of the embedding model
hf_model = HuggingFaceEndpointEmbeddings(
    model = model_name,
    huggingfacehub_api_token = os.getenv("HF_TOKEN")
)

# Loading of the data
db = Chroma(persist_directory =  "vectorstore",
            embedding_function = hf_model,
            collection_name= "portofolio_collection")

# results = db.similarity_search(query = "Who is Christian", k = 3)
# print(type(results[0]))
# for r in results:
#     print("=========")
#     print(r.page_content)
#     print(r.metadata)
#     print("=========")

# Creation of the retierver
retriever = db.as_retriever(
    search_type = "mmr", # to find the most simmilary but also different chunks
    search_kwargs = { "k":5, # maximum number of value returned
                     "fetch_k":15 , # number of chunks to select first before chosing
                     "lambda_mult": 0.7 # diversity of the result
                    }
)


# Loading of the model
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature = 0.2,
)


# === CONTEXT MANAGMENT ===
# (using Redis)

r = redis.Redis.from_url(os.getenv("REDIS_URL"))

# Get the history from the Redis and add  it on the local history for the LLM
def get_session_history(session_id : str) -> ChatMessageHistory:
    chat = r.get(f"chat:{session_id}")
    history = ChatMessageHistory()

    if chat :
        dicts = json.loads(chat)
        messages = messages_from_dict(dicts)
        history.add_messages(messages)
        
    return history

# Save the history of the session on Redis
def save_session_history(session_id: str, history : ChatMessageHistory):
    r.set(f"chat:{session_id}", json.dumps(messages_to_dict(history.messages)), ex=3600) # expire après 1h

# === CREATION OF THE PROMPT AND LAUNCHING ===

# Creation of the prompt
system_prompt = """
You are Onyx, the AI assistant embedded in Christian BOSSE's personal portfolio website.
Your role is to help visitors (recruiters, collaborators, curious people) learn about Christian's background, skills, projects, and experience.
You are currently a chatbot, but you will be developed into a complete AI assistant.

Your personality:
- Warm, professional, and approachable
- Enthusiastic about Christian's work without being arrogant
- Concise but thorough: give enough detail to be helpful, not more

Rules:
1. Base your answers ONLY on the context below and on the conversation history. Never invent facts about Christian (dates, companies, grades, skills, etc.).
2. If the context only covers part of the question, answer what you know and clearly say what is missing.
3. If the context contains nothing useful, say something like:
   "Humm... I don't have that information yet, but you can reach Christian directly at christianbosse123@gmail.com or on LinkedIn: https://www.linkedin.com/in/christian-bosse-6104a9332/ for more details 😊"
4. Always respond in the same language as the user's question.
5. If the user greets you (e.g. "Hello", "Salut"), respond warmly and briefly introduce yourself and what you can help with.
6. Use the conversation history to understand follow-up questions (e.g. "and his internship?", "tell me more").
7. Topics that are IN SCOPE: Christian's education, experience, skills, projects, availability, goals, mindset, hobbies, contact, this portfolio and this chatbot (how it was built, its stack).
    If you are in doubt, consider the question in scope and try to answer.
8. Only refuse requests that are clearly unrelated to Christian (e.g. math problems, recipes, politics, writing code for the user, general trivia). In that case, politely redirect in your own words, for example:
   "That's a bit outside my area! 🤔 I could answer but ... I'm here to talk about Christian's profile. Feel free to ask about his skills, projects, education or experience."
9. Generic technical questions (e.g. "What is RAG?", "What is ML") can be answered in 1-2 sentences, then linked back to Christian's work if relevant.
10. Format your answers for readability:
   - Use bullet points (•) for lists
   - Use bold for key information (names of schools, job titles, technologies)
   - Keep paragraphs short (2-3 sentences max)
   - Add spacing between sections

Context:
{context}
"""

prompt = ChatPromptTemplate([
    ("system", system_prompt),
    MessagesPlaceholder("chat_history", n_messages = 20),
    ("human","{query}")
])

# Improvement of the query given by the user
condense_prompt = ChatPromptTemplate([
    ("system",
     "Given the conversation history and the user's latest question, rewrite the "
     "question so it is fully standalone (understandable without the history). "
     "The conversation is about Christian BOSSE. "
     "Do NOT answer the question. Return ONLY the rewritten question, in the same language. "
     "If the question is already standalone, return it unchanged."),
    MessagesPlaceholder("chat_history", n_messages=5),
    ("human", "{query}")
])

# Reformulation chain
condense_chain = condense_prompt | llm | StrOutputParser()

# Function to transform Document type into string
def doc_to_str(documents):
    return "\n\n".join([doc.page_content for doc in documents])

# Rewrites the question only if there is a history
def contextualize(inputs):
    if not inputs.get("chat_history"):
        return inputs["query"]          # first message: nothing to rewrite
    return condense_chain.invoke(inputs)

# RAG Chain
setup = {
    "context": RunnableLambda(contextualize) | retriever | doc_to_str ,
    "query" : itemgetter("query"),
    "chat_history": itemgetter("chat_history")
}

rag_chain = setup | prompt | llm | StrOutputParser()

# answer = rag_chain.invoke("C'est quoi le mindset de Christian ?")
# print("ANSWER :\n",answer)