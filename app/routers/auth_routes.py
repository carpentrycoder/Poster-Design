# ==============================
# routers/auth_routes.py
# Owner login aur authentication handle karta hai
# JWT token generate karta hai
# ==============================

from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
import os
from jose import jwt
from dotenv import load_dotenv
from app.schemas import LoginRequest, TokenResponse

# .env file ka exact path do (project root mein hai)
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Router object banao
router = APIRouter(
    prefix="/auth",    # Saare routes /auth se shuru honge
    tags=["Authentication"]  # Swagger docs mein grouping
)

# .env se settings load karo
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "admin")
OWNER_PASSWORD = os.getenv("OWNER_PASSWORD", "admin123")
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def create_access_token(data: dict) -> str:
    """
    JWT Token banao.
    Token mein user info encode hoti hai + expiry time.
    """
    to_encode = data.copy()

    # Token kab expire hoga
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Token encode karo (sign karo)
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# ==============================
# POST /auth/login
# Owner login endpoint
# ==============================
@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    """
    Owner login kare.

    - username aur password check karo
    - sahi hain toh JWT token return karo
    - galat hain toh error do
    """

    # Username aur password verify karo
    if credentials.username != OWNER_USERNAME or credentials.password != OWNER_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Galat username ya password! Dobara try karo.",
        )

    # Token banao
    token = create_access_token(data={"sub": credentials.username})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        message="Login successful! Dashboard access mil gaya."
    )