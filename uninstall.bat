@echo off
echo ===================================================
echo  Uninstalling / Cleaning Unemployment Analysis App
echo ===================================================
echo.
echo WARNING: This will delete the virtual environment (.venv) and downloaded data files.
set /p confirm="Are you sure you want to proceed? (Y/N): "
if /i "%confirm%" neq "Y" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo [1/3] Removing virtual environment (.venv)...
if exist .venv (
    rmdir /s /q .venv
    echo Virtual environment removed.
) else (
    echo No virtual environment found.
)

echo.
echo [2/3] Removing downloaded dataset files...
if exist data (
    rmdir /s /q data
    echo Data folder removed.
) else (
    echo No data folder found.
)

echo.
echo [3/3] Removing Python cache directories...
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    rmdir /s /q "%%d"
)
echo Cache cleaned.

echo.
echo ===================================================
echo  Cleanup finished successfully!
echo ===================================================
echo.
pause
