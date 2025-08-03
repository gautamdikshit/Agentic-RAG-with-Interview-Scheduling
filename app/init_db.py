# app/init_db.py
from app.database import Base, engine
from app.models.booking import Booking
from app.models.metadata import Metadata
from app.models.query_metadata import QueryMetadata

Base.metadata.create_all(bind=engine)
