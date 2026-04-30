# 🎨 Poster Design Order Management System

FastAPI + SQLite + Bootstrap se banaya hua simple aur beginner-friendly order management system!

---

## 📁 Project Structure

```
poster_design_fastapi/
│
├── app/
│   ├── main.py          ← FastAPI app entry point
│   ├── database.py      ← Database connection
│   ├── models.py        ← Database table structure
│   ├── schemas.py       ← Request/Response format
│   ├── crud.py          ← Database operations + price logic
│   │
│   ├── routers/
│   │   ├── order_routes.py   ← /orders API
│   │   └── auth_routes.py    ← /auth/login API
│   │
│   ├── templates/       ← HTML pages (Jinja2)
│   │   ├── base.html
│   │   ├── index.html   ← Customer form
│   │   ├── login.html   ← Owner login
│   │   └── dashboard.html ← Orders table
│   │
│   └── static/
│       ├── css/style.css
│       ├── js/script.js
│       └── images/      ← Uploaded images yahan save hongi
│
├── .env                 ← Secret settings
├── requirements.txt     ← Python packages
└── README.md
```

---

## 🚀 Setup & Run

### Step 1: Python virtual environment banao

```bash
# Virtual environment create karo
python -m venv venv

# Activate karo
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 2: Dependencies install karo

```bash
pip install -r requirements.txt
```

### Step 3: Project folder mein jao

```bash
cd poster_design_fastapi
```

### Step 4: Server start karo

```bash
uvicorn app.main:app --reload
```

**For Production (Render):**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Step 5: Browser mein kholo

| Page | URL |
|------|-----|
| Customer Form | http://localhost:8000/ |
| Owner Login | http://localhost:8000/login |
| Dashboard | http://localhost:8000/dashboard |
| API Docs | http://localhost:8000/docs |

---

## 🔑 Default Login

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |

> `.env` file mein badal sakte ho!

---

## 💰 Price Logic

```
Total = Font Price + Poster Size Price

Font Prices:
  Handwritten = ₹30
  Bold        = ₹20
  Elegant     = ₹40
  Modern      = ₹25
  Classic     = ₹35

Size Prices:
  A4     = ₹100
  A3     = ₹150
  A2     = ₹200
  A1     = ₹300
  Custom = ₹250
```

---

## 🌐 API Endpoints

| Method | URL | Kya karta hai |
|--------|-----|----------------|
| POST | `/orders/` | Naya order submit karo |
| GET | `/orders/` | Saare orders dekho |
| GET | `/orders/{id}` | Ek specific order |
| GET | `/orders/download?format=csv` | CSV download |
| GET | `/orders/download?format=json` | JSON download |
| GET | `/orders/price-info` | Price list |
| POST | `/auth/login` | Owner login |
| GET | `/docs` | Swagger API docs |

---

## 📦 Technologies Used

- **FastAPI** — Python web framework
- **SQLite** — Database (no installation needed!)
- **SQLAlchemy** — Database ORM
- **Jinja2** — HTML templating
- **Bootstrap 5** — Frontend styling
- **JWT** — Authentication tokens
- **Python-dotenv** — Environment variables

---

## 🎓 SEPM Concepts

- **Client-Server Architecture**: Frontend → API → Backend → Database
- **Modular Design**: Order, Auth, Price modules alag hain
- **REST API**: Standard HTTP methods use kar rahe hain
- **MVC Pattern**: Models, Routers (Controllers), Templates (Views)

---

## ❓ Problems? 

1. `ModuleNotFoundError` → `pip install -r requirements.txt` dobara run karo
2. Port busy hai → `uvicorn app.main:app --reload --port 8001` try karo
3. Database error → `poster_orders.db` file delete karo, app restart karo