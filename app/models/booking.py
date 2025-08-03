# app/models/booking.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)


