from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database import Base
from datetime import datetime

class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    chunking_method = Column(String, nullable=False)
    embedding_model = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.now)
