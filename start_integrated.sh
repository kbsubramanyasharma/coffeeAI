#!/bin/bash

# Integrated startup script for Coffee AI - Backend + Frontend

echo "🚀 Starting Coffee AI Integrated System..."

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Check if ports are available
echo "🔍 Checking port availability..."
if ! check_port 8000; then
    echo "❌ Backend port 8000 is already in use. Please stop the service using port 8000."
    exit 1
fi

if ! check_port 5173; then
    echo "❌ Frontend port 5173 is already in use. Please stop the service using port 5173."
    exit 1
fi

# Start backend server
echo "🔧 Starting Backend Server (RAG Chat API)..."
cd chatbot_rag-main

# Check if Python dependencies are installed
if [ ! -f "poetry.lock" ]; then
    echo "📦 Installing Python dependencies..."
    poetry install
fi

# Start backend in background
echo "🌐 Backend starting on http://localhost:8000"
python main.py --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! check_port 8000; then
    echo "✅ Backend server started successfully"
else
    echo "❌ Failed to start backend server"
    exit 1
fi

# Go back to root directory
cd ..

# Start frontend server
echo "🎨 Starting Frontend Server..."
echo "🌐 Frontend starting on http://localhost:5173"

# Start frontend in background
npm run dev &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 5

# Check if frontend started successfully
if ! check_port 5173; then
    echo "✅ Frontend server started successfully"
else
    echo "❌ Failed to start frontend server"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 Coffee AI Integrated System is running!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep script running
wait 