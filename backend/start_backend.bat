@echo off
REM AQUA Guardian - Backend Startup Script for Windows
REM This script activates the virtual environment and starts the FastAPI backend server

echo ==========================================
echo AQUA Guardian - Starting Backend Server
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run the setup first:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment and start server
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Starting FastAPI server on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start uvicorn server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

REM Deactivate on exit
deactivate
