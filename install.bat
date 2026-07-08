@echo off
echo ===================================================
echo  Installing Dependencies for Unemployment Analysis
echo ===================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in system PATH.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

:: Create virtual environment
echo [1/3] Creating Python Virtual Environment (.venv)...
python -m venv .venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

:: Upgrade pip and install requirements
echo.
echo [2/3] Activating environment and upgrading pip...
call .venv\Scripts\activate
python -m pip install --upgrade pip

echo.
echo [3/3] Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo  Installation completed successfully!
echo  You can now run 'run.bat' to launch the dashboard.
echo ===================================================
echo.
pause
