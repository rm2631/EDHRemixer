#!/bin/bash
set -e

echo "🔨 Building EDHRemixer Application..."

# Build Angular frontend
echo "📦 Building Angular frontend..."
cd frontend
npm install
npm run build
cd ..

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
cd api
pip install -r requirements.txt
cd ..

echo "✅ Build complete!"
echo ""
echo "To run the application:"
echo "  cd api && gunicorn app:app"
echo ""
echo "The application will serve on port 5000 (or PORT env variable)"
