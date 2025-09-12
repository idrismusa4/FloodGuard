## Deploy FloodGuard: Single Service on Render

1) Push this repo to GitHub/GitLab.

2) In Render, create a Blueprint from the repo. It will detect `render.yaml` and create:
   - Web Service `floodguard-app` (FastAPI + React via Docker)

3) Set environment variables in Render:
   - `SUPABASE_URL`, `SUPABASE_KEY`, `EARTH2_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `MAPS_API_KEY`.
   - `ENVIRONMENT=production` (already set in blueprint; verify)
   - `REACT_APP_API_URL` = leave empty (uses relative URLs in production)

4) Deploy. The service will:
   - Build React frontend and serve it via Nginx
   - Run FastAPI backend on port 8000
   - Proxy API requests from Nginx to FastAPI
   - Serve everything on port 80

5) Access your app:
   - Frontend: `<service-url>/` (e.g., https://floodguard-app.onrender.com/)
   - API: `<service-url>/health`, `<service-url>/docs`, etc.

Notes
- Single Docker container serves both frontend and backend
- Nginx handles SPA routing and API proxying
- No CORS issues since everything runs on the same domain


