@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Python environment is missing. Follow README.md first.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" "scripts\stop_app.py"
pause
