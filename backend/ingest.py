#!/usr/bin/env python3
import os
import shutil

from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
# help(PyPDFLoader)

# == INITIALIZATION ==
CV = "../data/CVs/CV_BOSSE_July_3_eng.pdf"
model_name    = "sentence-transformers/all-MiniLM-L6-v2" # name of the model to use from huggingface
model_kwargs  = {"device":"cuda"}
encode_kwargs = {"normalize_embeddings": True}

# ==== LOADINGS ====

# Loading of the CV
cv_loader = PyPDFLoader(CV)
document = cv_loader.load()

# Loading the different part of the portofolio
portofolio_loader = DirectoryLoader("../data", glob="**/*.md", loader_cls=TextLoader)
document += portofolio_loader.load()

print("Number of document loaded :",len(document))


# === CREATION OF THE VECTOR DARA BASE ===
# delete of the last vector base
if os.path.exists("vectorstore"):
    shutil.rmtree("vectorstore")
    print("==> Last Vectorestore deleted.")

# Splitting the data into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
    length_function= len,
)

chunks = text_splitter.split_documents(document)

# creation of the embeddings
hf_model = HuggingFaceEmbeddings(
    model_name = model_name,
    model_kwargs = model_kwargs,
    encode_kwargs = encode_kwargs
)

db = Chroma.from_documents(
    documents = chunks,
    embedding = hf_model,
    collection_name = "portofolio_collection",
    persist_directory = "vectorstore/",
)
print("==> Vector data base succesfuly created.")

# test
results = db.similarity_search(query = "what are my programming languages ?", k = 3)

for r in results:
    print()
    print(r.page_content)
    print(r.metadata)
    print("----")