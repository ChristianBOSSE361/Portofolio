#!usr/env/bin python3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatbot import *
    
# creation of the application
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://christianbosse361.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Structure of the question
class QuestionRequest(BaseModel):
    question : str
    session_id : str

# The endpoints
@app.get("/")
def read_root():
    return {"message": "Portofolio API RAG online .... "}


@app.post("/api/chat")
def chat_endpoint(query : QuestionRequest):

    # get of the history
    history = get_session_history(query.session_id)
    
    # generation of the answer
    answer = rag_chain.invoke( { "query" : query.question , "chat_history" : history.messages })

    # adding the information in the history
    history.add_message(HumanMessage(query.question))
    history.add_message(AIMessage(answer))

    # saving the history of the session 
    save_session_history(query.session_id, history)

    return {"answer": answer}