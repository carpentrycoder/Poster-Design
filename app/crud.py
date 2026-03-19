# ==============================
# crud.py
# CRUD = Create, Read, Update, Delete
# Database operations yahan hoti hain
# ==============================

from sqlalchemy.orm import Session
from app import models, schemas


# ==============================
# Price Calculation
# ==============================

# Font styles aur unki prices
FONT_PRICES = {
    "handwritten": 30,
    "bold": 20,
    "elegant": 40,
    "modern": 25,
    "classic": 35,
}

# Poster sizes aur unki prices
SIZE_PRICES = {
    "a4": 100,
    "a3": 150,
    "a2": 200,
    "a1": 300,
    "custom": 250,
}


def calculate_price(font_style: str, poster_size: str) -> float:
    """
    Font aur Size ke hisaab se total price calculate karo.

    Example:
        font = handwritten (30) + size = a4 (100) = 130 total
    """
    font_price = FONT_PRICES.get(font_style.lower(), 25)  # default 25 agar match na ho
    size_price = SIZE_PRICES.get(poster_size.lower(), 100)  # default 100
    return float(font_price + size_price)


# ==============================
# Create Order
# ==============================

def create_order(db: Session, order: schemas.OrderCreate, image_path: str = None) -> models.Order:
    """
    Naya order database mein save karo.

    Steps:
    1. Price calculate karo
    2. Order object banao
    3. Database mein save karo
    4. Return karo
    """
    # Price calculate karo
    price = calculate_price(order.font_style, order.poster_size)

    # Database model object banao
    db_order = models.Order(
        customer_name=order.customer_name,
        phone=order.phone,
        email=order.email,
        poster_reason=order.poster_reason,
        font_style=order.font_style,
        poster_size=order.poster_size,
        total_price=price,
        image_path=image_path,
    )

    # Database mein add karo
    db.add(db_order)
    db.commit()              # Save karo
    db.refresh(db_order)     # ID aur timestamp fetch karo

    return db_order


# ==============================
# Get All Orders
# ==============================

def get_all_orders(db: Session) -> list:
    """
    Saare orders fetch karo (newest pehle).
    Owner dashboard ke liye use hoga.
    """
    return db.query(models.Order).order_by(models.Order.created_at.desc()).all()


# ==============================
# Get Single Order
# ==============================

def get_order_by_id(db: Session, order_id: int) -> models.Order:
    """
    ID se ek specific order dhundo.
    """
    return db.query(models.Order).filter(models.Order.id == order_id).first()