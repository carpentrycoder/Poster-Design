# ==============================
# database.py
# Database se connection setup karta hai
# SQLite use kar rahe hain - koi installation nahi chahiye!
# ==============================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# .env file se variables load karo
load_dotenv()

# Database URL - must be set in environment variables for security
# Never include hardcoded credentials in source code!
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please configure it in .env or your deployment platform.")

# Engine banao - yeh database se actual connection hai
engine = create_engine(
    DATABASE_URL
    # connect_args={"check_same_thread": False}  # SQLite ke liye zaroori hai - PostgreSQL ke liye nahi
)

# Session factory - har request ke liye ek session milega
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class - sare models isse inherit karenge
Base = declarative_base()


# ==============================
# Dependency Function
# FastAPI routes mein use hogi
# ==============================
def get_db():
    """
    Database session do aur kaam khatam hone ke baad band karo.
    FastAPI automatically 'finally' block call karta hai.
    """
    db = SessionLocal()
    try:
        yield db  # route function ko db de do
    finally:
        db.close()  # kaam khatam, connection band karo