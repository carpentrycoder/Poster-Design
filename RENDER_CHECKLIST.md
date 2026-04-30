# 📋 Render Deployment Checklist

## Pre-Deployment Checklist

### Code Quality
- [ ] No hardcoded credentials in code (use .env)
- [ ] DATABASE_URL in .env file
- [ ] All environment variables documented in .env.example
- [ ] No console.log/print statements for sensitive data
- [ ] Code pushed to GitHub

### Configuration Files Present
- [ ] `Procfile` exists with correct start command
- [ ] `render.yaml` exists with deployment config
- [ ] `.env` file has DATABASE_URL and other secrets
- [ ] `.env.example` exists as template
- [ ] `.gitignore` protects .env file
- [ ] `requirements.txt` has all dependencies (including gunicorn)

### Dependencies
- [ ] `gunicorn==21.2.0` in requirements.txt
- [ ] `python-dotenv==1.0.1` for .env loading
- [ ] `psycopg2-binary==2.9.9` for PostgreSQL
- [ ] All FastAPI dependencies present

### Database
- [ ] PostgreSQL database ready (Neon)
- [ ] DATABASE_URL is valid and tested
- [ ] Database user has CREATE TABLE permissions

### Cloudinary
- [ ] CLOUDINARY_CLOUD_NAME set in .env
- [ ] CLOUDINARY_API_KEY set in .env
- [ ] CLOUDINARY_API_SECRET set in .env

### Security
- [ ] SECRET_KEY changed from default
- [ ] OWNER_PASSWORD is strong
- [ ] ALLOWED_ORIGINS configured for production
- [ ] No debug=True in production settings

---

## Deployment Steps (Render Dashboard)

1. **Create Web Service**
   - Connect GitHub repo
   - Select Python runtime
   - Python version: 3.11

2. **Configure Build**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.index:app`

3. **Set Environment Variables**
   - Copy all values from .env
   - Paste into Render dashboard

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Check logs for errors

---

## Verification After Deployment

### API Health Check
```bash
curl https://your-app.onrender.com/api
```

### Check Documentation
- Swagger: https://your-app.onrender.com/docs
- ReDoc: https://your-app.onrender.com/redoc

### Database Connection
- Try creating an order: POST /orders
- Check if orders are saved in database

### Image Upload Test
- Upload image through /orders endpoint
- Verify Cloudinary upload works

---

## Environment Variables for Render

Copy-paste this into Render dashboard:

```
DATABASE_URL=postgresql://neondb_owner:npg_Mc9GbDiwJuX0@ep-winter-heart-ad1jblng-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

OWNER_USERNAME=admin
OWNER_PASSWORD=admin123

SECRET_KEY=meri-secret-key-123-poster-app
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

CLOUDINARY_CLOUD_NAME=dn2vdgzgs
CLOUDINARY_API_KEY=559744156969371
CLOUDINARY_API_SECRET=MF0a2lAcV6bmPHZsSyZAQdoXh0U

ALLOWED_ORIGINS=*
```

---

## Project Files Summary

```
Poster-Design/
├── Procfile                          # Render start command
├── render.yaml                       # Render deployment config
├── .env                              # ⚠️ SECRET - Don't commit
├── .env.example                      # Template for .env
├── .gitignore                        # Protects .env
├── DEPLOYMENT.md                     # This guide
├── requirements.txt                  # Python packages
├── alembic.ini                       # Database migrations
├── api/
│   └── index.py                      # Mangum handler for Vercel
├── app/
│   ├── main.py                       # FastAPI app (fixed)
│   ├── database.py                   # DB config (fixed - no hardcoded credentials)
│   ├── models.py                     # SQLAlchemy models
│   ├── schemas.py                    # Pydantic schemas
│   ├── crud.py                       # Database operations
│   ├── routers/
│   │   ├── auth_routes.py            # Login endpoint
│   │   └── order_routes.py           # Orders API
│   ├── static/                       # CSS, JS, Images
│   └── templates/                    # HTML pages
└── README.md                         # Original project docs
```

---

## Common Issues & Solutions

### Issue: "DATABASE_URL environment variable is not set"
**Solution**: Add DATABASE_URL to Render Environment Variables

### Issue: Module not found (e.g., "No module named 'app'")
**Solution**: Ensure requirements.txt has all packages, rebuild on Render

### Issue: Static files not loading
**Solution**: Ensure paths in templates are correct

### Issue: App works locally but not on Render
**Solution**: Check Render logs for specific error messages

---

## Quick Deploy Command

After setting up Render dashboard:
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
# Render auto-deploys when you push!
```

---

✅ You're ready to deploy! Follow DEPLOYMENT.md for detailed steps.
