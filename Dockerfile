# Single-stage production Dockerfile for Digital Ocean
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    gcc \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for frontend build
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy and install backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend/

# Copy and build frontend
COPY frontend/package*.json ./frontend/
WORKDIR /app/frontend
RUN npm install --legacy-peer-deps

COPY frontend/ .
RUN npm run build

# Back to app root
WORKDIR /app

# Copy nginx configuration
COPY nginx.conf /etc/nginx/sites-available/default

# Copy start script
COPY start.sh .
RUN chmod +x start.sh

# Expose ports
EXPOSE 80 8000

# Start the application
CMD ["./start.sh"]
