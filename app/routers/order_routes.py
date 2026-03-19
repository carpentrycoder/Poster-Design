# ==============================
# routers/order_routes.py
# Customer orders ke saare API endpoints
# Ab Cloudinary se image upload hogi!
# ==============================

import os
import csv
import json
import cloudinary
import cloudinary.uploader
from pathlib import Path
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app import crud, schemas

# .env file load karo (exact path de rahe hain)
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# ==============================
# Cloudinary Setup
# ==============================
cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key    = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure     = True
)

# Router banao
router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# ==============================
# Helper Function: Cloudinary Upload
# ==============================
async def upload_image_to_cloudinary(image: UploadFile) -> str:
    """
    Image file Cloudinary pe upload karo.
    Wapas secure URL milega jo DB mein save hoga.

    Example URL:
    'https://res.cloudinary.com/your-cloud/image/upload/v123/poster_images/abc.jpg'
    """
    image_bytes = await image.read()

    upload_result = cloudinary.uploader.upload(
        image_bytes,
        folder="poster_images",
        resource_type="image",
        use_filename=True,
        unique_filename=True,
    )

    return upload_result["secure_url"]


# ==============================
# POST /orders
# Naya order submit karo
# ==============================
@router.post("/", response_model=schemas.MessageResponse)
async def create_order(
    customer_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    poster_reason: str = Form(...),
    font_style: str = Form(...),
    poster_size: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Customer ka naya poster order submit karo.

    Steps:
    1. Image ho toh Cloudinary pe upload karo → URL lo
    2. Order schema banao
    3. Database mein save karo (image_url bhi)
    4. Success response bhejo
    """

    # ===== Image Upload to Cloudinary =====
    image_url = None

    if image and image.filename:
        try:
            image_url = await upload_image_to_cloudinary(image)
            print(f"Image uploaded: {image_url}")
        except Exception as e:
            # Upload fail hone pe bhi order save hoga, sirf image nahi hogi
            print(f"Cloudinary upload failed: {e}")
            image_url = None

    # ===== Order Save Karo =====
    order_data = schemas.OrderCreate(
        customer_name=customer_name,
        phone=phone,
        email=email,
        poster_reason=poster_reason,
        font_style=font_style,
        poster_size=poster_size,
    )

    new_order = crud.create_order(db=db, order=order_data, image_path=image_url)

    return schemas.MessageResponse(
        message="Order successfully submit ho gaya! Hum aapka poster banayenge.",
        order_id=new_order.id,
        total_price=new_order.total_price,
    )


# ==============================
# GET /orders
# ==============================
@router.get("/", response_model=list[schemas.OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    return crud.get_all_orders(db=db)


# ==============================
# GET /orders/price-info
# ==============================
@router.get("/price-info")
def get_price_info():
    return {
        "font_prices": crud.FONT_PRICES,
        "size_prices": crud.SIZE_PRICES,
        "message": "Font Price + Size Price = Total Price"
    }


# ==============================
# GET /orders/download
# ==============================
@router.get("/download")
def download_orders(format: str = "csv", db: Session = Depends(get_db)):
    orders = crud.get_all_orders(db=db)

    if format.lower() == "json":
        data = [{
            "id": o.id,
            "customer_name": o.customer_name,
            "phone": o.phone,
            "email": o.email,
            "poster_reason": o.poster_reason,
            "font_style": o.font_style,
            "poster_size": o.poster_size,
            "total_price": o.total_price,
            "image_url": o.image_path,
            "created_at": str(o.created_at),
        } for o in orders]

        filepath = "/tmp/orders.json"
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        return FileResponse(filepath, filename="poster_orders.json", media_type="application/json")

    else:
        filepath = "/tmp/orders.csv"
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Phone", "Email", "Reason", "Font", "Size", "Price", "Image URL", "Date"])
            for o in orders:
                writer.writerow([o.id, o.customer_name, o.phone, o.email,
                    o.poster_reason, o.font_style, o.poster_size,
                    o.total_price, o.image_path or "No image", o.created_at])
        return FileResponse(filepath, filename="poster_orders.csv", media_type="text/csv")


# ==============================
# GET /orders/{order_id}
# ==============================
@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order #{order_id} nahi mila!")
    return order