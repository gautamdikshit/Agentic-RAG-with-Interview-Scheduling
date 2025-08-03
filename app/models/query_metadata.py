from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database import Base

class QueryMetadata(Base):
    __tablename__ = "query_metadata"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String)
    retrieval_time = Column(Float)
    latency = Column(Float)

