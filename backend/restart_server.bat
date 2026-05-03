@echo off
echo ======================================================================
echo RESTARTING FASTAPI SERVER WITH NEW CREDENTIALS
echo ======================================================================
echo.
echo Step 1: Checking environment configuration...
python check_env.py
echo.
echo Step 2: Please STOP the running server in Terminal 1 or 2 (press Ctrl+C)
echo.
echo Step 3: After stopping, run this command in the terminal:
echo    cd Alebaple-codecompass/backend
echo    python -m uvicorn app.main:app --reload --port 8000
echo.
echo Step 4: Then run the test:
echo    python test_final_api.py
echo.
echo ======================================================================
pause

@REM Made with Bob
