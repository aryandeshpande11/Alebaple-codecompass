# PowerShell script to restart server and test
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "RESTARTING FASTAPI SERVER WITH NEW IBM WATSONX.AI CREDENTIALS" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check environment
Write-Host "Step 1: Checking environment configuration..." -ForegroundColor Yellow
cd Alebaple-codecompass/backend
python check_env.py
Write-Host ""

# Step 2: Kill existing uvicorn processes
Write-Host "Step 2: Stopping existing FastAPI servers..." -ForegroundColor Yellow
$processes = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*uvicorn*"}
if ($processes) {
    $processes | Stop-Process -Force
    Write-Host "[SUCCESS] Stopped existing servers" -ForegroundColor Green
} else {
    Write-Host "[INFO] No running servers found" -ForegroundColor Gray
}
Start-Sleep -Seconds 2
Write-Host ""

# Step 3: Start new server
Write-Host "Step 3: Starting FastAPI server with new credentials..." -ForegroundColor Yellow
Write-Host "[INFO] Server will start in a new window..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python -m uvicorn app.main:app --reload --port 8000"
Start-Sleep -Seconds 5
Write-Host ""

# Step 4: Run tests
Write-Host "Step 4: Testing real API integration..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
python test_final_api.py
Write-Host ""

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "RESTART COMPLETE" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Made with Bob
