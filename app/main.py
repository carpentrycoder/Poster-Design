# ==============================
# main.py
# FastAPI Application ka Entry Point
# Yahan se poora app start hota hai
# ==============================

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database import engine, Base
from app.routers import order_routes, auth_routes

# ==============================
# Database Tables Banao
# App start hote hi tables create honge (agar nahi hain toh)
# ==============================
Base.metadata.create_all(bind=engine)

# ==============================
# FastAPI App Instance
# ==============================
app = FastAPI(
    title="Poster Design Order System",
    description="Customer poster orders manage karne ka system",
    version="1.0.0",
)

# ==============================
# CORS Middleware
# Frontend aur Backend different ports pe ho toh bhi kaam kare
# Production mein specific domain dena
# ==============================
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],       # GET, POST, PUT, DELETE sab allowed
    allow_headers=["*"],
)

# ==============================
# Static Files Mount
# CSS, JS, Images serve karne ke liye
# ==============================
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ==============================
# Jinja2 Templates
# HTML files render karne ke liye
# ==============================
templates = Jinja2Templates(directory="app/templates")

# ==============================
# Routers Include Karo
# Alag alag route files ko main app mein add karo
# ==============================
app.include_router(order_routes.router)   # /orders routes
app.include_router(auth_routes.router)    # /auth routes


# ==============================
# HTML Page Routes
# ==============================

@app.get("/")
def home(request: Request):
    """Customer Order Form Page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login")
def login_page(request: Request):
    """Owner Login Page"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard")
def dashboard_page(request: Request):
    """Owner Dashboard Page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


# ==============================
# Root API Check
# ==============================
@app.get("/api")
def api_root():
    """API check karo - kaam kar raha hai ya nahi"""
    return {
        "message": "Poster Design API chal rahi hai! 🎨",
        "docs": "/docs",
        "status": "running"
    }