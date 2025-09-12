# Multi-stage Docker build for FloodGuardian AI

# Backend Stage
FROM python:3.11-slim as backend

WORKDIR /app/backend

# Install system dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

# Expose backend port
EXPOSE 8000

# Command to run the backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Frontend Stage
FROM node:18-alpine as frontend

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies (use npm install for broader CI compatibility)
RUN npm install --legacy-peer-deps

# Copy frontend source code
COPY frontend/ .

# Build the frontend
RUN npm run build

# Production Stage
FROM python:3.11-slim as production

WORKDIR /app

# Install system dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    gcc \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Copy built frontend from frontend stage
COPY --from=frontend /app/frontend/build ./frontend/build

# Copy nginx configuration (use conf.d to avoid managing sites-enabled symlinks)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose ports
EXPOSE 80 8000

# Start script
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]

