import os
import shutil
from pathlib import Path
import builtins
from sys import platform as pltfrm_type
import json
from dotenv import load_dotenv

load_dotenv()

LINUX_MNT = Path("/projects") ### change this if needed, to use the mount in a linux environment
USER_DRIVE = Path("C:")
USER = Path(str(Path.home()).split("\\")[-1])

NETWORK_ROOT_FOLDER = Path("/XX")
WIN_FOLDER = Path("/Users")
ROOT_FOLDER = Path("Documents") 
SLSH = os.path.sep
BKSLH = "/"

if pltfrm_type in ['win32', 'cygwin']:
    BASE_MNT = USER_DRIVE
else:
    BASE_MNT = LINUX_MNT

BASEPATH_NETWORK = str(BASE_MNT) + str(NETWORK_ROOT_FOLDER)

BASE_MNT = USER_DRIVE
BASEPATH_USER = r"" / BASE_MNT / WIN_FOLDER / USER / ROOT_FOLDER

BASEPATH = BASEPATH_NETWORK

DB_USER = os.getenv("DB_USER")
DB_PASSWORD_DEV = os.getenv("DB_PASSWORD_DEV")
DB_HOST_DEV = os.getenv("DB_HOST_DEV")
DB_PASSWORD_LIVE = os.getenv("DB_PASSWORD_LIVE")
DB_HOST_LIVE = os.getenv("DB_HOST_LIVE")