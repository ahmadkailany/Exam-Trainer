@echo off
rem Exam Trainer v1.0.0 - made by Ahmad Kailany for 42 Students
if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" "%~dp0examshell.py" %*
) else (
    python "%~dp0examshell.py" %*
)
