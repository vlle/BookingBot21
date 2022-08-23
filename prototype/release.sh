#!/bin/bash
if [ ! -f sqlite3.db ]; then
    echo "DB not found!"
    bash database/reset_database.sh
fi
python3 -m venv check_venv
source check_venv/bin/activate
pip install -r requirements.txt
python bot.py 
