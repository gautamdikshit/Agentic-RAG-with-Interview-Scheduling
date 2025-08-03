from langchain_community.vectorstores import Pinecone as PineconeStore
from app.config import INDEX_NAME, PINECONE_ENVIRONMENT
from app.deps import embeddings, pc

def store_documents(documents):
    if INDEX_NAME not in pc.list_indexes().names():
        # pc.create_index(name=INDEX_NAME, dimension=384, metric="cosine")
        pc.create_index(name="index_euclidean", dimension=384, metric="euclidean")


    vectorstore = PineconeStore.from_documents(
        documents=documents,
        embedding=embeddings,
        index_name=INDEX_NAME
    )

    return vectorstore

