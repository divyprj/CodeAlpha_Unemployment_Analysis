@echo off
echo ===================================================
echo  Running Unemployment Analysis Application
echo ===================================================
echo.

:: Check if virtual environment exists
if not exist .venv\Scripts\activate.bat (
    echo [ERROR] Virtual environment not found. Please run 'install.bat' first.
    pause
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

:: Download/Verify data files
echo.
echo Checking dataset files...
python download_data.py
if %errorlevel% neq 0 (
    echo [WARNING] Problem with data files. Let's try to proceed anyway.
)

:: Run Streamlit App
echo.
echo Launching Streamlit Dashboard...
streamlit run app.py

pause
