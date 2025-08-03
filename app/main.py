from fastapi import FastAPI
from app.api import upload, chat
import os 
import uvicorn
from app.config import LANGCHAIN_API_KEY

# Langsmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"

app = FastAPI(title="RAG Backend with Agentic Reasoning")

# Include routers
app.include_router(upload.router)
app.include_router(chat.router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
