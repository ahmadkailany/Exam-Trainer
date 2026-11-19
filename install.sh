#!/bin/sh
# Exam Trainer v1.0.0 - made by Ahmad Kailany for 42 Students
# Linux / macOS installer: creates .venv and installs the requirements.
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
    echo "[Exam Trainer] python3 was not found - please install Python 3."
    exit 1
fi
python3 examshell.py --install || exit 1
echo
echo "[Exam Trainer] Ready! Start it with:  make   (or: python3 examshell.py)"
