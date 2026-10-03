#!usr/env/bin python3
import os
import redis
import json

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import  RunnablePassthrough
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
    search_kwargs = { "k":3, # maximum number of value returned
                     "fetch_k":10 , # number of chunks to select first before chosing
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
You are currently just a chatbot but you will be developed and became a completed AI assiatant.

Your personality:
- Warm, professional, and approachable
- Enthusiastic about Christian's work without being arrogant
- Concise but thorough - give enough detail to be helpful, not more

Rules:
1. ONLY use information from the context below to answer. Never invent or guess facts about Christian.
2. If the context does not contain the answer, say something like:
   "Humm... I don't have that information yet, but you can reach Christian directly at christianbosse123@gmail.com or on LinkedIn: https://www.linkedin.com/in/christian-bosse-6104a9332/ to have more information 😊."
3. Always respond in the same language as the user's question.
4. If the user greets you (e.g. "Hello", "Salut"), respond warmly and briefly introduce yourself and what you can help with.
5. If the user asks something completely unrelated to Christian (e.g. math, politics, cooking), politely redirect:
   "I could answer that question but... I'm specialized in answering questions about Christian's profile. Feel free to ask about his skills, projects, education, or experience!"
6. Format your answers for readability:
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

# Function to transform Document type into string
def doc_to_str(documents):
    return "\n\n".join([doc.page_content for doc in documents])

# RAG Chain
setup = {
    "context": itemgetter("query") | retriever | doc_to_str ,
    "query" : itemgetter("query") | RunnablePassthrough()
}

rag_chain = setup | prompt | llm | StrOutputParser()

# answer = rag_chain.invoke("C'est quoi le mindset de Christian ?")
# print("ANSWER :\n",answer)

