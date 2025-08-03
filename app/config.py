# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
# INDEX_NAME = os.getenv("INDEX_NAME", "ragbackendtest")
INDEX_NAME = os.getenv("INDEX_NAME", "indexeuclidean")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
OWNER_EMAIL = os.getenv("OWNER_EMAIL")

REDIS_URL = os.getenv("REDIS_URL")

LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
