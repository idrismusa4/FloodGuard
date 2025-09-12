## Deploy FloodGuard: Backend (Render) + Frontend (Vercel)

1) Push this repo to GitHub/GitLab.

2) In Render, create a Blueprint from the repo. It will detect `render.yaml` and create:
   - Web Service `floodguard-backend` (FastAPI only)

3) Set environment variables in Render (backend):
   - `SUPABASE_URL`, `SUPABASE_KEY`, `EARTH2_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `MAPS_API_KEY`.
   - `ENVIRONMENT=production` (already set in blueprint; verify)
   - `ALLOWED_ORIGINS` = your Vercel domain(s), comma-separated (e.g. `https://floodguard-frontend.vercel.app,https://www.yourdomain.com`).

4) Deploy. The backend binds to `$PORT` automatically.

### Frontend on Vercel
1) In Vercel, import the repo and set the project root to `frontend`.
2) Build Command: `npm run build` (Vercel detects CRA). Output Directory: `build`.
3) Add Environment Variable: `REACT_APP_API_URL` = your Render backend URL (e.g. `https://floodguard-backend.onrender.com`).
4) Deploy. SPA routing is handled by `vercel.json`.

Notes
- CORS is currently `*` in `backend/main.py`. Tighten for production if needed.
- `frontend/static.json` enables SPA routing on Render, serving `index.html` for client routes.


