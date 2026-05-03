@echo off
echo ======================================================================
echo Restarting Server with New IBM watsonx.ai Credentials
echo ======================================================================
echo.
echo Stopping any running servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting server...
cd /d "%~dp0"
start "FastAPI Server" cmd /k "python -m uvicorn app.main:app --reload --port 8000"

echo.
echo Waiting for server to start...
timeout /t 5 /nobreak >nul

echo.
echo Running API test...
python test_final_api.py

echo.
echo ======================================================================
echo Test complete! Check results above.
echo ======================================================================
pause

@REM Made with Bob
