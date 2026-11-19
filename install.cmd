@echo off
rem Exam Trainer v1.0.0 - made by Ahmad Kailany for 42 Students
rem Windows installer: creates .venv and installs the requirements.
where python >nul 2>nul
if errorlevel 1 (
    echo [Exam Trainer] Python 3 was not found. Install it from https://www.python.org/downloads/
    echo                and tick "Add python.exe to PATH" during the setup.
    pause
    exit /b 1
)
python "%~dp0examshell.py" --install
if errorlevel 1 (
    pause
    exit /b 1
)
echo.
echo [Exam Trainer] Ready! Start it with:  examshell   (or: make)
