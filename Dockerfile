# Multi-stage Dockerfile for Render deployment
# Stage 1: Build Angular frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Copy frontend source and build
COPY frontend/ ./
RUN npm run build

# Stage 2: Python backend with built frontend
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY api/requirements.txt ./api/
RUN pip install --no-cache-dir -r api/requirements.txt

# Copy application code
COPY api/ ./api/
COPY models/ ./models/

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist/frontend/browser ./frontend/dist/frontend/browser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/health')"

# Start gunicorn
CMD cd api && gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
