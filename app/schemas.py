# ==============================
# schemas.py
# Request aur Response data ka format define karta hai
# Pydantic use karta hai - automatic validation hoti hai
# ==============================

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ==============================
# Order Schemas
# ==============================

class OrderCreate(BaseModel):
    """
    Jab customer order submit karta hai toh yeh data aata hai.
    Yeh schema validate karega ki sab fields sahi hain.
    """
    customer_name: str        # Customer ka naam
    phone: str                # Phone number
    email: str                # Email address
    poster_reason: str        # Poster kisliye chahiye
    font_style: str           # Font style choice
    poster_size: str          # Poster size choice


class OrderResponse(BaseModel):
    """
    Jab order successfully create ho jaaye toh yeh response bhejte hain.
    """
    id: int
    customer_name: str
    phone: str
    email: str
    poster_reason: str
    font_style: str
    poster_size: str
    total_price: float
    image_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy objects ko Pydantic mein convert kare


# ==============================
# Auth Schemas (Login)
# ==============================

class LoginRequest(BaseModel):
    """Owner login ke liye username aur password"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Successful login ke baad token return karte hain"""
    access_token: str
    token_type: str = "bearer"
    message: str = "Login successful!"


# ==============================
# Generic Response
# ==============================

class MessageResponse(BaseModel):
    """Simple message response ke liye"""
    message: str
    order_id: Optional[int] = None
    total_price: Optional[float] = None