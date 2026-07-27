#!usr/env/bin python3
import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import  RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv


# === INITIALIZATION ===
model_name    = "sentence-transformers/all-MiniLM-L6-v2" # name of the model to use from huggingface
model_kwargs  = {"device":"cpu"}
encode_kwargs = {"normalize_embeddings": True}

# Loading the API key
load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise ValueError(" API KEY NOT FOUND !!!")

# Loading of the embedding model
hf_model = HuggingFaceEmbeddings(
    model_name = model_name,
    model_kwargs = model_kwargs,
    encode_kwargs = encode_kwargs
)

# Loading of the data
db = Chroma(persist_directory =  "vectorstore",
            embedding_function = hf_model,
            collection_name= "portofolio_collection")

results = db.similarity_search(query = "Who is Christian", k = 3)
print(type(results[0]))
for r in results:
    print("=========")
    print(r.page_content)
    print(r.metadata)
    print("=========")

# Creation of the retierver
retriever = db.as_retriever(
    search_type = "mmr", # to find the most simmilary but also different chunks
    search_kwargs = { "k":3, # maximum number of value returned
                     "fetch_k":10 , # number of chunks of to select first before chosing
                     "lambda_mult": 0.7 # diversity of the result
                    }
)


# Loading of the model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature = 0.2,
)

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
   - Use bold (**text**) for key information (names of schools, job titles, technologies)
   - Keep paragraphs short (2-3 sentences max)
   - Add spacing between sections

Context:
{context}
"""


prompt = ChatPromptTemplate([
    ("system", system_prompt),
    ("human","{query}")
])

# Function to transform Document type into string
def doc_to_str(documents):
    return "\n\n".join([doc.page_content for doc in documents])

# RAG Chain
setup = {
    "context": retriever | doc_to_str ,
    "query" : RunnablePassthrough()
}

rag_chain = setup | prompt | llm | StrOutputParser()

# answer = rag_chain.invoke("C'est quoi le mindset de Christian ?")
# print("ANSWER :\n",answer)

