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
You are an AI assistant, a Chatbot named Onyx aims to answer questions and preocupation of users about the persons who made this 
chat bot : Christian BOSSE.
Currently you are only a chatbot.
But your goal won't be only to answer question on me, but new features will be added to make you more complete and great.

Instruction:
1. Do not invent answer, just use the content of context to answer the question
2. If the answer is not in the context, stay polite and say that Christian did not give you this information yet.
3. Be concise, clear, professional, kind, repectful and friendly
4. Always answer in the same language as the question

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

