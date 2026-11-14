@echo off
title SafePulse AI - Cloudflare Public HTTPS Tunnel
echo ========================================================
echo  SafePulse AI - Cloudflare Port Forwarding Tunnel
echo ========================================================
echo.
echo Forwarding http://localhost:5173 (Frontend + API Proxy)...
echo Any device (mobile/laptop) can open this URL without setup!
echo.

set "CF_BIN=%~dp0cloudflared.exe"

if not exist "%CF_BIN%" (
    where cloudflared >nul 2>nul
    if %errorlevel% equ 0 (
        set "CF_BIN=cloudflared"
    ) else (
        echo Cloudflare binary not found. Downloading official cloudflared.exe...
        powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile '%~dp0cloudflared.exe'"
        if not exist "%~dp0cloudflared.exe" (
            echo [ERROR] Failed to download cloudflared.exe automatically.
            echo Please check your internet connection.
            pause
            exit /b 1
        )
        set "CF_BIN=%~dp0cloudflared.exe"
    )
)

echo Starting tunnel. Look for the public URL ending with '.trycloudflare.com' below:
echo =========================================================================
echo.

"%CF_BIN%" tunnel --url http://localhost:5173

echo.
echo Tunnel closed.
pause
