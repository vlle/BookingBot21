#!/bin/bash

python3 -m venv check_venv
source check_venv/bin/activate
pip install -r requirements.txt
python bot.py 
