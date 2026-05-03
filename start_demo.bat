@echo off
echo ============================================================
echo   Code Understanding and Onboarding Accelerator
echo   Starting Demo Environment
echo ============================================================
echo.

REM Check if backend virtual environment exists
if not exist "backend\.venv" (
    echo [ERROR] Backend virtual environment not found!
    echo Please run: cd backend ^&^& python -m venv .venv ^&^& .venv\Scripts\activate ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "frontend\node_modules" (
    echo [ERROR] Frontend dependencies not installed!
    echo Please run: cd frontend ^&^& npm install
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist "backend\.env" (
    echo [WARNING] Backend .env file not found!
    echo Copying from .env.example...
    copy "backend\.env.example" "backend\.env"
    echo.
    echo [ACTION REQUIRED] Please edit backend\.env with your watsonx.ai credentials
    pause
)

echo [1/3] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && .venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 5 /nobreak >nul

echo [2/3] Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"
timeout /t 5 /nobreak >nul

echo [3/3] Opening Browser...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo ============================================================
echo   Demo Environment Started Successfully!
echo ============================================================
echo.
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/api/docs
echo.
echo   Press Ctrl+C in each terminal window to stop servers
echo ============================================================
echo.
pause

@REM Made with Bob
