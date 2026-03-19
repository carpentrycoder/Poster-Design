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

# Database URL (SQLite file-based database) - commented out
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./poster_orders.db")

# Neon PostgreSQL URL - using environment variable for security
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_Mc9GbDiwJuX0@ep-winter-heart-ad1jblng-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

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