@echo off
REM Integrated startup script for Coffee AI - Backend + Frontend (Windows)

echo 🚀 Starting Coffee AI Integrated System...

REM Check if ports are available
echo 🔍 Checking port availability...

REM Check port 8000 (backend)
netstat -an | find "8000" >nul
if %errorlevel% equ 0 (
    echo ❌ Backend port 8000 is already in use. Please stop the service using port 8000.
    pause
    exit /b 1
)

REM Check port 5173 (frontend)
netstat -an | find "5173" >nul
if %errorlevel% equ 0 (
    echo ❌ Frontend port 5173 is already in use. Please stop the service using port 5173.
    pause
    exit /b 1
)

REM Start backend server
echo 🔧 Starting Backend Server (RAG Chat API)...
cd chatbot_rag-main

REM Check if Python dependencies are installed
if not exist "poetry.lock" (
    echo 📦 Installing Python dependencies...
    poetry install
)

REM Start backend in background
echo 🌐 Backend starting on http://localhost:8000
start "Backend Server" python main.py --port 8000

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Go back to root directory
cd ..

REM Start frontend server
echo 🎨 Starting Frontend Server...
echo 🌐 Frontend starting on http://localhost:5173

REM Start frontend in background
start "Frontend Server" npm run dev

REM Wait a moment for frontend to start
timeout /t 5 /nobreak >nul

echo.
echo 🎉 Coffee AI Integrated System is running!
echo.
echo 📱 Frontend: http://localhost:5173
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop both servers...

pause

REM Stop servers (this is a simple approach - in production you'd want more sophisticated process management)
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1

echo ✅ Servers stopped
pause 