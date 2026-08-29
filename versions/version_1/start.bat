@echo off
echo ===================================================
echo   Starting GeM Bid Analyzer Full-Stack Application
echo ===================================================

echo [1/3] Starting FastAPI Backend on Port 8000...
cd backend
if not exist venv (
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
)
start "Backend" cmd /k "venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"

echo [2/3] Starting Next.js Frontend on Port 3000...
cd ..\frontend
if not exist node_modules (
    call npm install
)
start "Frontend" cmd /k "npm run dev"

echo [3/3] Application Launch Triggered!
echo Backend API Docs: http://localhost:8000/docs
echo Frontend Web UI:  http://localhost:3000
