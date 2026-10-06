#!/usr/bin/env bash
# One time setup for macOS and Linux. Run: bash setup.sh
set -e
echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
echo "Installing packages (takes a few minutes)..."
python -m pip install --upgrade pip
pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
python scripts/check_setup.py
echo
echo "Done. Each time you open a new terminal, run:  source .venv/bin/activate"
