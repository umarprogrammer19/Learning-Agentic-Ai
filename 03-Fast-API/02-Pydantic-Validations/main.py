from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from datetime import datetime
from uuid import uuid4
from typing import List, Optional

app = FastAPI(
    title="DACA Chatbot App",
    description="A FastAPI-based API for a chatbot in the DACA tutorial series",
    version="0.1.0",
)


class MetaData(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: str = Field(default_factory=lambda: str(uuid4()))


class Message(BaseModel):
    user_id: str
    text: str
    metadata: MetaData
    tags: Optional[List[str]] = None


class Response(BaseModel):
    user_id: str
    reply: str
    metadata: MetaData


@app.get("/")
async def root():
    return {
        "message": "Welcome to the DACA Chatbot API! Access /docs for the API documentation."
    }


@app.get("/users/{user_id}")
async def get_user(user_id: str, role: Optional[str] = None):
    user_info = {"user_id": user_id, "role": role if role else "guest"}
    return user_info


@app.post("/chat/")
async def chat(message: Message):
    if not message.text.strip():
        raise HTTPException(status_code=400, detail="Message text cannot be empty")
    reply_text = f"Hello, {message.user_id}! You said: '{message.text}'. How can I assist you today?"
    return Response(
        user_id=message.user_id,
        reply=reply_text,
        metadata=MetaData(), 
    )
