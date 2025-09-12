## Deploy FloodGuard to Render

1) Push this repo to GitHub/GitLab.

2) In Render, create a Blueprint from the repo. It will detect `render.yaml` and create:
   - Web Service `floodguard-backend` (FastAPI)
   - Static Site `floodguard-frontend` (React build)

3) Set environment variables in Render:
   - On `floodguard-backend` service: `SUPABASE_URL`, `SUPABASE_KEY`, `EARTH2_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `MAPS_API_KEY`. `ENVIRONMENT` is set to `production` in the blueprint.
   - On `floodguard-frontend` static site: `REACT_APP_API_URL` pointing to the backend URL (e.g. `https://floodguard-backend.onrender.com`).

4) Deploy. The backend binds to `$PORT` automatically and the frontend is published from `frontend/build`.

Notes
- CORS is currently `*` in `backend/main.py`. Tighten for production if needed.
- `frontend/static.json` enables SPA routing on Render, serving `index.html` for client routes.


