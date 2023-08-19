title Create a virtual environment
:: Create a virtual environment
@echo off
echo "Started"

set ENV_STEM="venv"
::echo "Please enter a name to give your environment. The name should not have spaces"
::set /p "ENV_NAME=Environment name: "

set ENV_NAME=%ENV_STEM%

::%ENV_NAME%

echo "An environment with the name: %ENV_NAME% will be created"
pip install virtualenv
python -m virtualenv %ENV_NAME%
echo "Virtual environment created"
call .\%ENV_NAME%\Scripts\activate.bat
pip list
echo "Virtual environment activated"
python -m ensurepip --upgrade
python -m pip install --upgrade pip
pip list
pip install -r requirements.txt --no-cache
echo "Packages installed"
pip list

code .

pause

