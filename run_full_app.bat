@echo off
echo ==========================================
echo Starting WhatsApp Spark Dashboard
echo ==========================================

:: Start Backend
echo [1/3] Starting Flask Backend...
start "Flask Backend" cmd /c "cd backend && python app.py"

:: Start Frontend
echo [2/3] Starting React Frontend...
start "React Frontend" cmd /c "cd frontend && npm run dev"

:: Wait for servers to start
echo [3/3] Launching Browser...
timeout /t 5 /nobreak > nul
start http://localhost:5173

echo ==========================================
echo System is running!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo ==========================================
pause
