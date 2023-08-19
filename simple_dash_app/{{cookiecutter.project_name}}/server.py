from waitress import serve
import subprocess
import os
from sys import platform as pltfrm_type

print("Dash should be running on http://127.0.0.1:{{ cookiecutter.app_port }}/{{ cookiecutter.url_endpoint_of_app }}")
print("* Serving Flask app 'app'")
print("Press CTRL+C to quit")

if pltfrm_type in ['win32', 'cygwin']:
        subprocess.Popen("waitress-serve --listen=127.0.0.1:{{ cookiecutter.app_port }} app:app.server", shell=True, stdout=subprocess.PIPE, cwd=os.getcwd()).stdout.read()
else:
        subprocess.Popen("waitress-serve --port={{ cookiecutter.app_port }} --url-scheme=https app:app.server", shell=True, stdout=subprocess.PIPE, cwd=os.getcwd()).stdout.read()