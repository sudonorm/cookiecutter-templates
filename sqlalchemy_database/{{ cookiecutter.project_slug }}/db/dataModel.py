from __future__ import annotations

import inspect as sys_inspect
from sqlalchemy import create_engine, event, inspect, Index
from sqlalchemy.orm import declarative_base, registry, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData, Boolean, BigInteger, DateTime, Date, Numeric, Text, Float

from dataclasses import dataclass, field
from typing import List, Optional, Union
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import types
from sqlalchemy.dialects.mysql.base import MSBinary
import uuid
import subprocess

import os
import json
import re
import shutil
from pathlib import Path
import builtins
import sys
home_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(home_dir)
try:
    from .manager import Migrate, Connection
except:
    from manager import Migrate, Connection

from helper_functions import HelperFunctions

from resources import folderPaths
from sys import platform as pltfrm_type
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

RUN_ONLY_MIGRATION = folderPaths.RUN_ONLY_MIGRATION
IS_SQLITE = folderPaths.IS_SQLITE

LINUX_MNT = folderPaths.LINUX_MNT
USER_DRIVE = folderPaths.USER_DRIVE
USER = folderPaths.USER

NETWORK_ROOT_FOLDER = folderPaths.NETWORK_ROOT_FOLDER
WIN_FOLDER =  folderPaths.WIN_FOLDER
ROOT_FOLDER = folderPaths.ROOT_FOLDER
SLSH = folderPaths.SLSH
BKSLH = folderPaths.BKSLH 

BASEPATH_NETWORK = folderPaths.BASEPATH_NETWORK

BASEPATH = BASEPATH_NETWORK

helper_funcs = HelperFunctions()
con =  Connection()

mapper_registry = registry()
Base = mapper_registry.generate_base()

script_location = f'{home_dir}{folderPaths.SLSH}{"alembic"}'

if IS_SQLITE:
    sqlite_file = folderPaths.DB_NAME

    sqlite_file_path = f'{BASEPATH}{SLSH}{sqlite_file}'
    sqlite_file = sqlite_file_path
    db_uri = f"sqlite:///{sqlite_file_path}"
    
else:
    sqlite_file_path = ""
    db_uri = os.getenv("DB_URI")

engine = create_engine(db_uri, echo=False) # if you want to see the queries being executed, set echo=True (don't use echo=True in production)

##################################

SessionLocal = sessionmaker(bind=engine)

## replace Tables here
class TeatTable(Base):
    __tablename__ = "testTable"

    id = Column(Integer, primary_key=True)
    test_col = Column(String(200), nullable=False)

####### Do not delete ######
migrate = Migrate(script_location=script_location, uri=db_uri, is_sqlite=IS_SQLITE, db_file_path=sqlite_file_path, run_only_migration=RUN_ONLY_MIGRATION)
if migrate.check_for_migrations():
    migrate.init_db()