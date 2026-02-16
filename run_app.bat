@echo off
REM Target Allocation System - Startup Script for Windows
echo.
echo ========================================
echo  Target Allocation System - Startup
echo ========================================
echo.

REM Check if venv is activated
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup first.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Streamlit application...
echo Opening browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run app.py

pause
