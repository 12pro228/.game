@echo off
cd /d "%~dp0"

set "PYTHON=python"
if exist "%~dp0.venv\Scripts\python.exe" (
  set "PYTHON=%~dp0.venv\Scripts\python.exe"
)

"%PYTHON%" "%~dp0game.py"

if errorlevel 1 (
  echo.
  echo The game stopped because of an error.
  pause
)
