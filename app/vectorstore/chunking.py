from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_core.documents import Document

def extract_and_chunk_text(file_path: str, chunking_method, chunk_size=1000, chunk_overlap=200):
    reader = PdfReader(file_path)
    text = "".join(page.extract_text() or "" for page in reader.pages)

    if chunking_method.lower() == "character text splitter":
        splitter = CharacterTextSplitter(separator="\n", chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    elif chunking_method.lower() == "recursive":
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    chunks = splitter.split_text(text)
    
    return [Document(page_content=chunk) for chunk in chunks]
