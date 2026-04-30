# 🚀 Render Deployment Guide

## Step-by-Step Deployment to Render

### Prerequisites
- Render account (https://render.com)
- Git repository with this code
- Neon PostgreSQL database URL (already in .env)
- Cloudinary credentials (already in .env)

### Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Setup for Render deployment"
git push origin main
```

### Step 2: Create New Web Service on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Fill in the details:
   - **Name**: `poster-design-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.index:app`
   - **Instance Type**: `Free` (or `Standard` for production)

### Step 3: Set Environment Variables

In Render dashboard, go to **Environment** and add these variables:

```
DATABASE_URL = postgresql://... (copy from .env)
OWNER_USERNAME = admin
OWNER_PASSWORD = admin123
SECRET_KEY = your-secure-random-key (change this!)
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
CLOUDINARY_CLOUD_NAME = dn2vdgzgs
CLOUDINARY_API_KEY = 559744156969371
CLOUDINARY_API_SECRET = MF0a2lAcV6bmPHZsSyZAQdoXh0U
ALLOWED_ORIGINS = https://your-frontend-domain.com (or *)
```

**⚠️ WARNING**: Never commit `.env` file to Git. Only set secrets in Render dashboard!

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will automatically build and deploy
3. Check logs for any errors
4. Your app will be live at: `https://poster-design-api.onrender.com`

---

## ✅ After Deployment

### Test Your API
```bash
curl https://poster-design-api.onrender.com/api
```

Expected response:
```json
{
  "message": "Poster Design API chal rahi hai! 🎨",
  "docs": "/docs",
  "status": "running"
}
```

### Check Interactive Docs
- Swagger UI: `https://your-app.onrender.com/docs`
- ReDoc: `https://your-app.onrender.com/redoc`

---

## 🔧 Configuration Files

### render.yaml
- Auto-deployment configuration
- Environment variables setup
- Build and start commands

### Procfile
- Used by Render to start the app
- Specifies Gunicorn with Uvicorn workers

### .env.example
- Template for environment variables
- Copy and fill with actual values

---

## 📌 Important Notes

### Database Migrations (Alembic)
If you need to run migrations on Render:

1. Connect to Render shell:
   ```bash
   render exec -s poster-design-api -- /bin/bash
   ```

2. Run migrations:
   ```bash
   alembic upgrade head
   ```

### Free Tier Limitations
- App spins down after 15 min of inactivity
- Limited to 100 concurrent requests
- For production, upgrade to **Standard** or **Pro** plan

### Production Security Checklist
- [ ] Change `SECRET_KEY` to a random secure string
- [ ] Change `OWNER_PASSWORD` to a strong password
- [ ] Set `ALLOWED_ORIGINS` to specific domain instead of `*`
- [ ] Use strong database password
- [ ] Enable HTTPS (automatic on Render)
- [ ] Set up monitoring/logging

---

## 🆘 Troubleshooting

### App won't start
Check logs in Render dashboard. Common issues:
- Missing DATABASE_URL environment variable
- Missing required packages (check requirements.txt)
- Python version compatibility

### Database connection error
- Verify DATABASE_URL is correct
- Check Neon database is running
- Ensure Render IP is whitelisted (if needed)

### Static files not loading
- Ensure `app/static` directory exists
- Check CSS/JS paths in HTML templates

---

## 🎯 Environment Variables Quick Copy

Copy to Render dashboard:
```
DATABASE_URL=postgresql://neondb_owner:npg_Mc9GbDiwJuX0@ep-winter-heart-ad1jblng-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
OWNER_USERNAME=admin
OWNER_PASSWORD=admin123
SECRET_KEY=poster-app-secret-key-2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CLOUDINARY_CLOUD_NAME=dn2vdgzgs
CLOUDINARY_API_KEY=559744156969371
CLOUDINARY_API_SECRET=MF0a2lAcV6bmPHZsSyZAQdoXh0U
ALLOWED_ORIGINS=*
```

---

Happy Deploying! 🎉
