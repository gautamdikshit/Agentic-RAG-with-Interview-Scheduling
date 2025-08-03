# app/tools/booking_tool.py
import json, os, re, smtplib
from email.mime.text import MIMEText
from langchain_core.tools import tool
from app.config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, OWNER_EMAIL
from typing import Dict
from app.database import SessionLocal
from app.models.booking import Booking

BOOKING_FILE = "bookings.json"
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# Function to load the BOOKING_FILE 
def load_bookings() -> list:
    if not os.path.isfile(BOOKING_FILE):
        return []
    with open(BOOKING_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
        

# # Function to save booking details locally 
# def save_booking(entry: Dict):

#     bookings = load_bookings()
#     bookings.append(entry)
#     with open(BOOKING_FILE, "w", encoding="utf-8") as f:
#         json.dump(bookings, f, indent=2, ensure_ascii=False)

# Function to save to PostgreSQL Database 
def save_booking(entry: Dict):

    db = SessionLocal()
    try:
        booking = Booking(**entry)
        db.add(booking)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


# Function to send confirmation email 
def send_confirmation(to_email: str, full_name: str, date: str, time: str):

    body = (f"Hello {full_name},\n\n"
            f"This is a confirmation that your interview is scheduled on {date} at {time}.\n"
            f"We look forward to meeting you!\n\n"
            f"Best regards,\nThe Team")
    msg = MIMEText(body)
    msg["Subject"] = "Interview Confirmation"
    msg["From"]    = SMTP_USERNAME
    msg["To"]      = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, [to_email, OWNER_EMAIL], msg.as_string())

@tool
def book_interview_tool(full_name: str, email: str, date: str, time: str) -> str:
    """
    Book an interview and send a confirmation email.
    All four parameters are required.

    Args:
        full_name: candidate's full name
        email:     candidate's email address
        date:      desired date (YYYY-MM-DD)
        time:      desired time (HH:MM 24-hour format)
    Returns:
        success / error message
    """
    # Basic validation
    if not EMAIL_REGEX.match(email):
        return "Invalid e-mail address."

    entry = {
        "full_name": full_name,
        "email":     email,
        "date":      date,
        "time":      time,
    }

    try:
        save_booking(entry)
        send_confirmation(email, full_name, date, time)
    except Exception as e:
        return f"Booking stored locally, but mail failed: {e}"
    return "✅ Interview booked and confirmation e-mail sent!"
