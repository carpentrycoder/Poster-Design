# ==============================
# main.py
# FastAPI Application ka Entry Point
# ==============================

import os
import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# ==============================
# Logging Setup (IMPORTANT)
# ==============================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🚀 Starting Poster Design API...")

# ==============================
# Base Directory (Render Safe Paths)
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==============================
# Import DB & Routes
# ==============================
from app.database import engine, Base
from app.routers import order_routes, auth_routes

logger.info("✅ Database engine imported")

# ==============================
# Database Tables (SAFE MODE)
# ==============================
try:
    if os.getenv("RUN_DB_MIGRATION", "false") == "true":
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created/verified")
    else:
        logger.warning("⚠️ Skipping DB table creation (RUN_DB_MIGRATION=false)")
except Exception as e:
    logger.error(f"❌ DB Error: {e}")

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
# ==============================
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Static Files (FIXED PATH)
# ==============================
static_path = os.path.join(BASE_DIR, "static")

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    logger.info(f"✅ Static mounted: {static_path}")
else:
    logger.warning(f"⚠️ Static folder not found: {static_path}")

# ==============================
# Templates (FIXED PATH)
# ==============================
templates_path = os.path.join(BASE_DIR, "templates")

if not os.path.exists(templates_path):
    logger.error(f"❌ Templates folder missing: {templates_path}")

templates = Jinja2Templates(directory=templates_path)

# ==============================
# Routers
# ==============================
app.include_router(order_routes.router)
app.include_router(auth_routes.router)

logger.info("✅ Routers loaded")

# ==============================
# HTML Routes
# ==============================

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# ==============================
# API Health Check
# ==============================
@app.get("/api")
def api_root():
    return {
        "message": "Poster Design API chal rahi hai! 🎨",
        "docs": "/docs",
        "status": "running"
    }