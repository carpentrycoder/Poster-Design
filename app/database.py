# ==============================
# database.py
# Database se connection setup karta hai
# SQLite use kar rahe hain - koi installation nahi chahiye!
# ==============================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging
from dotenv import load_dotenv

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# .env file se variables load karo
load_dotenv()

# Database URL - must be set in environment variables for security
DATABASE_URL = os.getenv("DATABASE_URL")

logger.info(f"DATABASE_URL set: {bool(DATABASE_URL)}")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

# Fix postgres:// to postgresql:// for SQLAlchemy compatibility
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    logger.info("Converted postgres:// to postgresql://")

logger.info(f"Connecting to database...")

# Engine banao - with Neon/PostgreSQL optimizations
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Test connection before use
    pool_recycle=3600,   # Recycle connections after 1 hour
    connect_args={
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
    }
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