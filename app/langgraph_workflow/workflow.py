from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from app.langgraph_workflow.model_config import response_model, SYSTEM_PROMPT
from app.tools.booking_tool import book_interview_tool
from app.tools.retriever_tool import retriever_tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, ToolMessage
from app.langgraph_workflow.grader import grade_documents, rewrite_question, generate_answer



tools = [retriever_tool, book_interview_tool]

def generate_query_or_respond(state: MessagesState):
    """Call the model to generate a response based on the current state. Given
    the query, it will decide to use the given tools, or simply respond to the user."""

    messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(state['messages'])
    response = (response_model.bind_tools(tools).invoke(messages))

    return {"messages": [response]}


def which_tool_was_used(state: MessagesState) -> str:
    last_msg = state['messages'][-1]

    if isinstance(last_msg, ToolMessage):
        if last_msg.name == "book_interview_tool":
            return END
        elif last_msg.name == "retriever_tool":
            return "router"
    return END


workflow = StateGraph(MessagesState)

workflow.add_node(generate_query_or_respond)
workflow.add_node("tool_call", ToolNode(tools))
workflow.add_node("router", lambda state:state)
workflow.add_node("rewrite_question",rewrite_question)
workflow.add_node("generate_answer", generate_answer)

workflow.add_edge(START, "generate_query_or_respond")

workflow.add_conditional_edges(
    "generate_query_or_respond",
    tools_condition,
    {
        "tools": "tool_call",
        END : END
    }
)

workflow.add_conditional_edges(
    "tool_call",
    which_tool_was_used,
    {
        "router": "router",
        END: END
    }
)

workflow.add_conditional_edges(
    "router",
    grade_documents,
    {
        "rewrite_question": "rewrite_question",
        "generate_answer": "generate_answer"
    }
)
workflow.add_edge("generate_answer", END)
workflow.add_edge("rewrite_question", "generate_query_or_respond")

graph = workflow.compile()
