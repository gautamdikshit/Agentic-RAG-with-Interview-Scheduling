# 🧠 Agentic RAG with Interview Scheduling

This project implements a **modular and production-ready RAG (Retrieval-Augmented Generation)** backend system using **FastAPI**, featuring:

- Document upload with chunking and embedding
- Storage in **Pinecone** vector DB and metadata in **PostgreSQL**
- A LangGrpah-based **Agentic QA system** 
- Interview scheduling via conversational agent with email confirmation
- **No UI** — strictly backend APIs, ready for production

---

## 🔧 Tech Stack

- **Framework:** FastAPI
- **RAG Toolkit:** LangChain, LangGraph
- **Vector Store:** Pinecone
- **LLM**: ChatGroq (`llama3-8b-8192`)
- **Embedding Models:** `all-MiniLM-L6-v2`, `multi-qa-MiniLM-L6-cos-v1`
- **Chunking Strategies:** Recursive, Character Text Split
- **Database:** PostgreSQL (via SQLAlchemy)
- **Memory Layer:** Redis
- **Email:** SMTP via Gmail

---

## 🚀 API Overview

### 1. `/upload/` — File Upload & Processing

- **Method:** `POST`
- **Accepts:** `.pdf` or `.txt`
- **Steps:**
  - Extract text
  - Chunk via `recursive` or `character text splitter`
  - Embed using selected model
  - Store in **Pinecone**
  - Save metadata in PostgreSQL

### 2. `/chat/` — RAG Agent Interface

- **Method:** `POST`
- **Input:** user query
- **Process:**
  - Uses **LangGraph agent**
  - Selects tools (book_interview_tool, retriever_tool)
  - Maintains context with RedisMemory
  - Returns an LLM-generated response

---

## 📅 Interview Booking (Tool-Based Agent Step)

- Agent invokes booking tool when needed
- Collects: Full Name, Email, Date, Time
- Sends confirmation via SMTP to a pre-set email
- Saves booking data in PostgreSQL
- Validates date/time/email format

---

