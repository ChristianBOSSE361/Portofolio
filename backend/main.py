#!usr/env/bin python3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatbot import rag_chain

# creation of the application
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Structure of the question
class QuestionRequest(BaseModel):
    question : str

# The endpoints
@app.get("/")
def read_root():
    return {"message": "Portofolio API RAG online .... "}


@app.post("/api/chat")
def chat_endpoint(query : QuestionRequest):
    answer = rag_chain.invoke(query.question)
    return {"answer": answer}