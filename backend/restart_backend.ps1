# Restart Backend Server Script
# This script stops any running backend server and starts a fresh one

Write-Host "=== Restarting Backend Server ===" -ForegroundColor Cyan

# Kill any existing uvicorn processes
Write-Host "Stopping existing backend processes..." -ForegroundColor Yellow
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*uvicorn*"} | Stop-Process -Force

Start-Sleep -Seconds 2

# Navigate to backend directory
Set-Location -Path "Alebaple-codecompass/backend"

Write-Host "Starting backend server..." -ForegroundColor Green
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "" 
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
python -m uvicorn app.main:app --reload --port 8000

# Made with Bob
