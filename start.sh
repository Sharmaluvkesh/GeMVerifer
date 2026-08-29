#!/bin/bash
echo "==================================================="
echo "  Starting GeM Bid Analyzer Full-Stack Application"
echo "==================================================="

# Start Backend
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start Frontend
cd ../frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
npm run dev &
FRONTEND_PID=$!

echo ""
echo "Application Running!"
echo "Backend API Docs: http://localhost:8000/docs"
echo "Frontend Web UI:  http://localhost:3000"
echo ""

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
