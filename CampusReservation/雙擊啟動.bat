@echo off
echo ===================================================
echo   Campus Reservation System - Startup Script
echo ===================================================
echo.

:: 1. Detect Python
set "PYTHON_CMD="
python --version >nul 2>&1
if %errorlevel% EQU 0 set "PYTHON_CMD=python"

if "%PYTHON_CMD%"=="" (
    py --version >nul 2>&1
    if %errorlevel% EQU 0 set "PYTHON_CMD=py"
)

if "%PYTHON_CMD%"=="" (
    echo [ERROR] Python is not detected! Please ensure Python is installed and added to PATH.
    echo You can download Python from https://www.python.org/
    echo Make sure to check Add Python to PATH during installation.
    echo.
    pause
    exit /b
)

:: 2. Setup Virtual Environment
set "USE_VENV=0"
if exist .venv\Scripts\activate.bat set "USE_VENV=1"

if "%USE_VENV%"=="0" (
    echo [1/3] Creating Python virtual environment...
    %PYTHON_CMD% -m venv .venv
)

if exist .venv\Scripts\activate.bat (
    set "USE_VENV=1"
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    set "RUN_CMD=python"
)

if not exist .venv\Scripts\activate.bat (
    set "USE_VENV=0"
    set "RUN_CMD=%PYTHON_CMD%"
)

:: 3. Install Dependencies
echo [2/3] Installing and updating requirements...
if "%USE_VENV%"=="1" (
    python -m pip install --upgrade pip >nul 2>&1
    python -m pip install -r requirements.txt
)
if "%USE_VENV%"=="0" (
    %PYTHON_CMD% -m pip install --upgrade pip --user >nul 2>&1
    %PYTHON_CMD% -m pip install --user -r requirements.txt
)

:: 4. Initialize Database
if not exist database.db (
    echo [3/3] Database not found. Initializing database...
    %RUN_CMD% init_db.py
)
if exist database.db (
    echo [3/3] Database is ready.
)

:: 5. Start Server and Open Web Browser
echo Starting Flask server...
echo Once started, open http://127.0.0.1:5000 in your browser.
echo To close the application, simply close this window.
echo.

:: Open browser after a 2 second delay
start /b cmd /c "timeout /t 2 >nul && start http://127.0.0.1:5000"
%RUN_CMD% app.py

pause
