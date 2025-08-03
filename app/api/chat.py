from fastapi import APIRouter, Body
from app.langgraph_workflow.workflow import graph
from app.config import REDIS_URL
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import HumanMessage
import uuid

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
async def chat(message: str = Body(...), session_id: str = Body(default=None)):
    if session_id is None:
        session_id = str(uuid.uuid4())

    history = RedisChatMessageHistory(url=REDIS_URL, session_id=session_id)
    history.add_message(HumanMessage(content=message))

    messages = history.messages
    for chunk in graph.stream({"messages": messages}):
        for _, update in chunk.items():
            final_msg = update["messages"][-1]

    history.add_message(final_msg)
    return {
        "response": final_msg.content
    }
