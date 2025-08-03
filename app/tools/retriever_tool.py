from langchain_core.tools import tool
from app.deps import retriever
import time 
from app.database import SessionLocal
from app.models.query_metadata import QueryMetadata

@tool
def retriever_tool(query: str) -> str:
    """
    This tool searches and returns the information from the given pdf source.
    """
    start_time = time.time()

    docs = retriever.invoke(query)

    retrieval_time = time.time() - start_time

    # Save query_metadata in PostgreSQL
    db = SessionLocal()
    q_meta = QueryMetadata(
        query = query,
        retrieval_time = retrieval_time,
    )
    db.add(q_meta)
    db.commit()
    db.close()

    if not docs:
        return "I found no relevant information in the provided pdf."
    
    results = []

    for i, doc in enumerate(docs):
        results.append(f"Document {i+1}:\n {doc.page_content}")

    return "\n\n".join(results)