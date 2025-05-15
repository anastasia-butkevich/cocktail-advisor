from fastapi import FastAPI
from .models import ChatRequest, ChatResponse
from ..rag.rag import RAGSystem


app = FastAPI()
rag = RAGSystem()


@app.post("/chat", response_model=ChatResponse)
async def chat(input: ChatRequest):
    """Process chat messages and return cocktail information"""
    user_input = input.message
    response = rag.response(user_input)
    
    return ChatResponse(response=response.content)
