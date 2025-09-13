#!/bin/bash

# Start script for FloodGuardian AI production deployment

echo "🛡️ Starting FloodGuardian AI..."

# Start FastAPI (background)
echo "Starting FastAPI backend..."
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Optional: start flood monitor in background
# python jobs/flood_monitor.py --continuous &

# Start nginx in foreground (container stays alive)
echo "Starting Nginx..."
nginx -g "daemon off;"


# Wait for backend to be ready
echo "Waiting for backend to be ready..."
sleep 10

# Start the flood monitor job
echo "Starting flood monitoring job..."
python jobs/flood_monitor.py --continuous &

echo "✅ FloodGuardian AI is now running!"
echo "📊 Dashboard: http://localhost"
echo "🔌 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"

# Keep the container running
wait

