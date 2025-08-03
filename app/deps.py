# app/deps.py
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from app.config import PINECONE_API_KEY, INDEX_NAME
from langchain_community.vectorstores import Pinecone as PineconeStore

# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

embeddings = HuggingFaceEmbeddings(model_name="multi-qa-MiniLM-L6-cos-v1")


pc = Pinecone(api_key=PINECONE_API_KEY)


# Initialize retriever from vectorstore
retriever = PineconeStore.from_existing_index(
    index_name=INDEX_NAME,
    embedding=embeddings
).as_retriever()

