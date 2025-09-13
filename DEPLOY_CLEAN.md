# 🚀 Clean Deployment: Vercel (Frontend) + Digital Ocean (Backend)

## Overview
- **Frontend**: Vercel (React app)
- **Backend**: Digital Ocean (FastAPI)
- **Clean separation** with proper CORS configuration

---

## 📋 Prerequisites
1. Delete existing deployments on all platforms
2. Push clean code to GitHub
3. Have your environment variables ready

---

## 🔧 Backend on Digital Ocean

### Step 1: Create Backend Service
1. Go to [Digital Ocean Apps](https://cloud.digitalocean.com/apps)
2. Click **"Create App"**
3. Choose **"GitHub"** as source
4. Select your FloodGuard repository
5. Digital Ocean will detect `.do/app.yaml` automatically

### Step 2: Configure Backend
The app spec will create:
- **Service Name**: `backend`
- **Source Directory**: `backend`
- **Runtime**: Python
- **Build Command**: Auto-detected
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Port**: 8000

### Step 3: Set Environment Variables
In Digital Ocean → App Settings → Environment Variables, add these as **SECRET**:

```
SUPABASE_URL = your-supabase-url
SUPABASE_KEY = your-supabase-key
EARTH2_API_KEY = mock-earth2-key-for-development
TWILIO_ACCOUNT_SID = your-twilio-sid
TWILIO_AUTH_TOKEN = your-twilio-token
TWILIO_PHONE_NUMBER = your-twilio-number
MAPS_API_KEY = your-maps-key
ENVIRONMENT = production
ALLOWED_ORIGINS = *
```

### Step 4: Deploy Backend
1. Click **"Create Resources"**
2. Wait for deployment (5-10 minutes)
3. **Copy the backend URL** (e.g., `https://your-backend.ondigitalocean.app`)

---

## 🎨 Frontend on Vercel

### Step 1: Create Frontend Project
1. Go to [Vercel](https://vercel.com)
2. Click **"New Project"**
3. Import from GitHub → Select your FloodGuard repository
4. **Root Directory**: `frontend`

### Step 2: Configure Build Settings
Vercel will auto-detect:
- **Framework**: Create React App
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Install Command**: `npm install`

### Step 3: Set Environment Variable
In Vercel → Project Settings → Environment Variables:
```
REACT_APP_API_URL = https://your-backend.ondigitalocean.app
```
(Use the backend URL from Step 4 above)

### Step 4: Deploy Frontend
1. Click **"Deploy"**
2. Wait for build (2-3 minutes)
3. **Copy the frontend URL** (e.g., `https://your-app.vercel.app`)

---

## 🔒 Lock Down CORS (Optional)
After both are deployed:
1. In Digital Ocean, update `ALLOWED_ORIGINS` to your Vercel domain
2. Redeploy backend

---

## ✅ Verification

### Test Backend
- Health: `https://your-backend.ondigitalocean.app/health`
- API Docs: `https://your-backend.ondigitalocean.app/docs`
- Dashboard: `https://your-backend.ondigitalocean.app/dashboard/stats`

### Test Frontend
- Visit: `https://your-app.vercel.app`
- Dashboard should load with data
- All pages should work

---

## 🎯 Benefits of This Setup

✅ **Vercel Frontend**:
- Excellent React support
- Global CDN
- Automatic deployments
- Great performance

✅ **Digital Ocean Backend**:
- Simple Python deployment
- Good for APIs
- Reliable hosting
- Easy scaling

✅ **Clean Separation**:
- No Docker complexity
- Easy debugging
- Independent scaling
- Clear responsibilities

---

## 🆘 Troubleshooting

**Frontend can't reach backend**:
- Check `REACT_APP_API_URL` in Vercel
- Verify backend URL is correct
- Check CORS settings

**Backend not starting**:
- Check Digital Ocean build logs
- Verify all environment variables are set
- Check Python dependencies

**API calls failing**:
- Check browser network tab
- Verify backend is running
- Check CORS configuration

---

## 💰 Cost
- **Vercel**: Free tier (100GB bandwidth, 100GB-hours)
- **Digital Ocean**: $5/month (Basic plan)
- **Total**: $5/month for production-ready setup
