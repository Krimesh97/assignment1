@echo off
SET virtual_env_path=.\.venv
CALL %virtual_env_path%\Scripts\activate.bat
python main.py
CALL deactivate
PAUSE