import os
import shutil
from pathlib import Path
import builtins
from sys import platform as pltfrm_type
import json

## Linux
LINUX_MNT = Path("/projects")

## Windows
USER_DRIVE = Path("C:")
WIN_FOLDER = Path("/Users")

## OS agnostic path to home directory
USER = Path(str(Path.home()).split("\\")[-1])

## data folders
ROOT_FOLDER = Path("/Documents") 
NETWORK_ROOT_FOLDER = Path("/repos/")

## separators
SLSH = os.path.sep
BKSLH = "/"

if pltfrm_type in ['win32', 'cygwin']: ## Windows
    BASE_MNT = f'{str(USER_DRIVE)}{SLSH}{str(WIN_FOLDER)}{SLSH}{str(USER)}{SLSH}{str(ROOT_FOLDER)}'
elif pltfrm_type in ['darwin']: ## MacOS
    BASE_MNT = f'{str(USER)}{str(ROOT_FOLDER)}'
else: ## Linux
    BASE_MNT = LINUX_MNT

BASEPATH_NETWORK = str(BASE_MNT) + str(NETWORK_ROOT_FOLDER)

BASEPATH = BASEPATH_NETWORK

DB_NAME = "{{ cookiecutter.sqlite_database_name }}"
DB_NAME = f'{DB_NAME}{".db"}'
RUN_ONLY_MIGRATION = False
IS_SQLITE = {{ cookiecutter.is_sqlite }}