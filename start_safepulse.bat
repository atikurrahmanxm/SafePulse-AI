@echo off
title SafePulse AI Launcher
echo Starting SafePulse AI Backend (8000) and Frontend (5173)...

start "SafePulse AI - Backend (8000)" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
timeout /t 2 /nobreak >nul
start "SafePulse AI - Frontend (5173)" cmd /k "cd /d "%~dp0frontend" && npm.cmd run dev -- --port 5173 --host 127.0.0.1"

echo.
echo Both windows launched! Open http://127.0.0.1:5173 in your browser.
echo Press any key to close this launcher window (keep the other 2 windows open).
pause >nul

