from setuptools import find_packages
from cx_Freeze import setup, Executable
import uuid
import re
import os
from pathlib import Path

### TO-DO: add icon, and uncomment Icon fields

VERSION_NUMBER = '1.0.0'
SEP = r"\."
TARGET_NAME = f'{"APP_v"}{re.sub(SEP, "_", VERSION_NUMBER)}{".exe"}'

directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
]

msi_data = {
    # "Directory": directory_table,
    "ProgId": [
        ("Prog.Id", None, None, "Some Tool", "IconId", None),
    ],
    # "Icon": [
    #     ("IconId", "icon.ico"),
    # ],
}

options = {
    'build_exe': {
        'include_files': ['Pages/', 'alembic/', 'assets/', 'utils/', 
        (str(Path(os.getcwd())) + "\\.env", ".env"),
        (str(Path(os.getcwd())) + "\\alembic.ini", "alembic.ini"),], 
        #### include_files is very important and is the only way to include folders in the application. The folders included here are copied and packaged with the app
        'includes': [
            'cx_Logging', 'idna',
        ],
        'packages': [
            'asyncio', 'flask', 'jinja2', 'dash', 'sqlalchemy', 'plotly', 'waitress', 'scipy', 'sklearn', 'pandas'
        ],
        'excludes': ['tkinter']
    },
    'bdist_msi': {
            "add_to_path": True,
            "data": msi_data,
            # "environment_variables": [
            #     ("E_MYAPP_VAR", "=-*MYAPP_VAR", "1", "TARGETDIR")
            # ],
            "upgrade_code": str({uuid.uuid4()}), ### upgrade_code will be used to upgrade the app, if a new version is created
    }
}

executables = [
    Executable('app.py',
               base='console', ### this can also be "Win32GUI" or "console"
               targetName=TARGET_NAME,
            #    icon="icon.ico",
               shortcutName="Some Tool",
            shortcutDir="DesktopFolder",)
]

setup(
    name='MMT',
    packages=find_packages(),
    version=VERSION_NUMBER,
    description='python version of the some tool',
    executables=executables,
    options=options
)
