# Deploy FloodGuard: Frontend (Netlify) + Backend (Render)

This is the most reliable deployment approach - Netlify excels at frontend hosting and Render is good for APIs.

## Backend on Render

### 1) Deploy Backend
- Go to [Render](https://render.com) → Create New → Web Service
- Connect your GitHub repo
- Configure:
  - **Name**: `floodguard-backend`
  - **Root Directory**: `backend`
  - **Environment**: Python 3
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 2) Set Environment Variables
Add these as **Secret** variables:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `EARTH2_API_KEY`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `MAPS_API_KEY`
- `ENVIRONMENT` = `production`
- `ALLOWED_ORIGINS` = `*` (or your Netlify domain later)

### 3) Deploy and Get URL
- Click **Create Web Service**
- Wait for deployment (5-10 minutes)
- Copy the backend URL (e.g., `https://floodguard-backend.onrender.com`)

## Frontend on Netlify

### 1) Deploy Frontend
- Go to [Netlify](https://netlify.com) → Add new site → Import from Git
- Connect your GitHub repo
- Configure:
  - **Base directory**: `frontend`
  - **Build command**: `npm run build`
  - **Publish directory**: `frontend/build`

### 2) Set Environment Variable
- Go to Site settings → Environment variables
- Add: `REACT_APP_API_URL` = your Render backend URL from step 3 above

### 3) Deploy
- Click **Deploy site**
- Wait for build (2-3 minutes)
- Get your Netlify URL (e.g., `https://floodguard-frontend.netlify.app`)

## Optional: Lock Down CORS
- In Render backend settings, update `ALLOWED_ORIGINS` to your Netlify domain
- Redeploy backend

## Access Your App
- **Frontend**: Your Netlify URL (e.g., `https://floodguard-frontend.netlify.app`)
- **API**: Your Render URL (e.g., `https://floodguard-backend.onrender.com/health`)
- **API Docs**: `https://floodguard-backend.onrender.com/docs`

## Benefits of This Setup

✅ **Netlify**: 
- Excellent CDN and global performance
- Reliable builds and deployments
- Great for React apps
- Free tier is generous

✅ **Render**: 
- Good for APIs
- Simple deployment
- Free tier available
- Better than trying to run both in one container

✅ **Separation of Concerns**:
- Frontend and backend can scale independently
- Easier debugging and monitoring
- No complex Docker builds

## Troubleshooting

**Frontend can't reach API**:
- Check `REACT_APP_API_URL` is set correctly in Netlify
- Verify backend is running at the Render URL
- Check browser network tab for CORS errors

**Backend not starting**:
- Check Render build logs
- Verify all environment variables are set
- Check that requirements.txt is in the backend directory

**CORS errors**:
- Set `ALLOWED_ORIGINS` in Render to your Netlify domain
- Or temporarily set to `*` for testing

## Cost
- **Netlify**: Free tier (100GB bandwidth, 300 build minutes)
- **Render**: Free tier (750 hours/month, sleeps after 15min inactivity)
- **Total**: $0/month for development/testing
