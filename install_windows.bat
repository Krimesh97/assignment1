@echo off
SET virtual_env_path=.\.venv_
SET python_ver=3.10
CALL virtualenv %virtual_env_path% --python=%python_ver%
CALL %virtual_env_path%\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt
CALL deactivate
