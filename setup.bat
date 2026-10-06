@echo off
REM One time setup for Windows. Double click it or run: setup.bat
echo Creating virtual environment...
python -m venv .venv || (echo Python not found. Install Python 3.11+ and tick "Add to PATH". & exit /b 1)
call .venv\Scripts\activate
echo Installing packages (takes a few minutes)...
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
python scripts\check_setup.py
echo.
echo Done. Each time you open a new terminal, run:  .venv\Scripts\activate
