from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.graph import MessagesState
from app.langgraph_workflow.model_config import response_model
from app.langgraph_workflow.prompts import GENERATE_PROMPT, REWRITE_PROMPT, GRADE_PROMPT
from typing import Literal


class GradeDocuments(BaseModel):
    """Grade documents using a binary score for relevence check"""

    binary_score: str = Field(description="Relevance score: 'yes' if relevant, or 'no' if not relevant")

grader_model = ChatGroq(model="llama3-8b-8192", temperature=0)


def grade_documents(state: MessagesState) -> Literal["generate_answer", "rewrite_question"]:
    """Determine whether the retrieved docs are relevant to the question."""

    question = state['messages'][0].content
    context = state['messages'][-1].content

    prompt = GRADE_PROMPT.format(question=question, context=context)

    response = (grader_model.with_structured_output(GradeDocuments).invoke([{"role":"user", "content":prompt}]))

    score = response.binary_score

    if score == "yes":
        return "generate_answer"
    else:
        return "rewrite_question"
    

def rewrite_question(state: MessagesState):
    """Rewrite the original user question"""

    messages = state['messages']
    question = messages[0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{"role":"user", "content": prompt}])
    return {"messages": [{"role":"user", "content": response.content}]}


def generate_answer(state: MessagesState):
    """Generate an answer"""
    question = state['messages'][0].content
    context = state['messages'][-1].content
    prompt = GENERATE_PROMPT.format(question=question, context=context)
    response = response_model.invoke([{"role":"user", "content": prompt}])
    return {"messages":[response]}
