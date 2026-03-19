# ==============================
# models.py
# Database table ka blueprint hai
# SQLAlchemy se database table define karte hain
# ==============================

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Order(Base):
    """
    'orders' table ka model.
    Har customer order yahan store hoga.
    """

    __tablename__ = "orders"  # Database mein table ka naam

    # Primary key - auto increment hoga (1, 2, 3, ...)
    id = Column(Integer, primary_key=True, index=True)

    # Customer ki details
    customer_name = Column(String(100), nullable=False)   # Naam zaroori hai
    phone = Column(String(20), nullable=False)             # Phone zaroori hai
    email = Column(String(100), nullable=False)            # Email zaroori hai

    # Poster ki details
    poster_reason = Column(String(500), nullable=False)   # Kisliye chahiye poster
    font_style = Column(String(50), nullable=False)       # Font choice
    poster_size = Column(String(20), nullable=False)      # Size choice

    # Image URL (Cloudinary pe upload hone ke baad URL milta hai)
    image_path = Column(String(500), nullable=True)  # 500 chars - Cloudinary URL ke liye

    # Price - backend calculate karega
    total_price = Column(Float, nullable=False)

    # Timestamp - kab order aaya (automatic)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        """Debug ke liye readable representation"""
        return f"<Order id={self.id} name={self.customer_name} price={self.total_price}>"