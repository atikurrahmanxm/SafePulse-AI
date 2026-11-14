@echo off
title SafePulse AI Launcher
echo ========================================================
echo Starting SafePulse AI Backend (8000) and Frontend (5173)...
echo ========================================================

set "PY_CMD=python"
if exist "%~dp0backend\.venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0backend\.venv\Scripts\python.exe"
)

start "SafePulse AI - Backend (8000)" cmd /k "cd /d "%~dp0backend" && "%PY_CMD%" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
timeout /t 2 /nobreak >nul
start "SafePulse AI - Frontend (5173)" cmd /k "cd /d "%~dp0frontend" && npm.cmd run dev -- --port 5173 --host 127.0.0.1"

echo.
echo Both servers launched!
echo Backend:    http://127.0.0.1:8000/docs
echo Frontend:   http://127.0.0.1:5173
echo Public URL: Run 'start_tunnel.bat' for instant Cloudflare HTTPS Tunnel
echo.
echo Press any key to close this launcher window (keep the other 2 windows open).
pause >nul
