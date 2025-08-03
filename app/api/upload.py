from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
from app.vectorstore.chunking import extract_and_chunk_text
from app.vectorstore.store import store_documents
from app.database import SessionLocal
from app.models.metadata import Metadata

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    chunking_method: str = Form(),
    embedding_model: str = Form("multi-qa-MiniLM-L6-cos-v1")
):
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF or TXT files supported.")
    
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        documents = extract_and_chunk_text(temp_path, chunking_method) #currently supports only recursive and character text split
        store_documents(documents)

        # Save metadata in PostgreSQL
        db = SessionLocal()
        meta = Metadata(
            file_name=file.filename,
            chunking_method=chunking_method,
            embedding_model=embedding_model
        )
        db.add(meta)
        db.commit()
        db.close()

        return {"message": "File uploaded, indexed, and metadata saved"}
    
    finally:
        os.remove(temp_path)
