#!/bin/bash

# AI Studio Startup Script
# This script starts both backend and frontend

echo "🚀 Starting AI Studio..."

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Start backend in background
echo "📦 Starting Backend..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if curl -s http://127.0.0.1:8000/api/health > /dev/null; then
    echo "✅ Backend is running!"
else
    echo "❌ Backend failed to start!"
    kill $BACKEND_PID
    exit 1
fi

# Start frontend
echo "🎨 Starting Frontend..."
cd frontend
npm run tauri dev

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
