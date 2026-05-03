@echo off
echo Stopping any running servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting server with new credentials...
echo.
start "FastAPI Server" cmd /k "cd /d %~dp0 && python -m uvicorn app.main:app --reload --port 8000"

timeout /t 5 /nobreak >nul

echo.
echo Testing API...
python test_final_api.py

echo.
echo Done! Check the FastAPI Server window for initialization messages.
pause

@REM Made with Bob
