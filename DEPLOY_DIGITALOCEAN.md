# Deploy FloodGuard to Digital Ocean App Platform

## Option 1: Using App Spec (Recommended)

1) **Push your code to GitHub** (if not already done)

2) **Create App in Digital Ocean**:
   - Go to Digital Ocean → Apps → Create App
   - Choose "GitHub" as source
   - Select your FloodGuard repository
   - Digital Ocean will detect the `.do/app.yaml` file automatically
   - Review the configuration and click "Create Resources"

3) **Set Environment Variables**:
   - In the App dashboard → Settings → App-Level Environment Variables
   - Add these as **Encrypted** (SECRET) variables:
     - `SUPABASE_URL`
     - `SUPABASE_KEY` 
     - `EARTH2_API_KEY`
     - `TWILIO_ACCOUNT_SID`
     - `TWILIO_AUTH_TOKEN`
     - `TWILIO_PHONE_NUMBER`
     - `MAPS_API_KEY`
   - `ENVIRONMENT` and `REACT_APP_API_URL` are already set in the spec

4) **Deploy**:
   - Click "Deploy" or it will auto-deploy
   - Wait for build to complete (usually 5-10 minutes)

5) **Access your app**:
   - Frontend: `https://your-app-name.ondigitalocean.app/`
   - API: `https://your-app-name.ondigitalocean.app/health`
   - API Docs: `https://your-app-name.ondigitalocean.app/docs`

## Option 2: Manual Setup

1) **Create App**:
   - Digital Ocean → Apps → Create App
   - Source: GitHub → Select your repo
   - **Don't** use the detected app spec

2) **Configure Service**:
   - Service Type: Web Service
   - Source Directory: `/` (root)
   - Build Command: (leave empty - uses Dockerfile)
   - Run Command: `./start.sh`
   - Environment: Docker
   - Instance: Basic ($5/month)
   - HTTP Port: 80

3) **Add Environment Variables** (same as Option 1)

4) **Deploy**

## Benefits of Digital Ocean vs Render

✅ **More reliable** - Better uptime and fewer build failures  
✅ **Better Docker support** - Native Docker builds without issues  
✅ **Faster builds** - More powerful build infrastructure  
✅ **Better pricing** - $5/month for basic instance  
✅ **No cold starts** - Always-on instances  
✅ **Better logging** - More detailed build and runtime logs  

## Troubleshooting

- **Build fails**: Check the build logs in Digital Ocean dashboard
- **App won't start**: Verify all environment variables are set
- **API not working**: Check that REACT_APP_API_URL is empty (uses relative URLs)
- **CORS issues**: Shouldn't happen since everything runs on same domain

## Cost

- **Basic plan**: $5/month for always-on instance
- **Pro plan**: $12/month for better performance
- **No bandwidth charges** for reasonable usage
