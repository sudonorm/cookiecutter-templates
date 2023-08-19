import sys
# sys.path.append(".")
home_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(home_dir)

try:
    from manager import Migrate, Connection
except:
    from .manager import Migrate, Connection
from resources import folderPaths
import os
from sqlalchemy import create_engine
import time

RUN_MIGRATION = folderPaths.RUN_MIGRATION
CREATE_ONLY_MIGRATION_FILE = folderPaths.CREATE_ONLY_MIGRATION_FILE
DROP_ALEMBIC_TABLE_AND_STAMP_HEAD = folderPaths.DROP_ALEMBIC_TABLE_AND_STAMP_HEAD

IS_SQLITE = folderPaths.IS_SQLITE

if __name__ == '__main__':

    sqlite_file_path = ""
    db_uri = os.getenv("DB_URI")
    if IS_SQLITE:
        
        con = Connection()

        sqlite_file_path = f'{folderPaths.BASEPATH_NETWORK}{folderPaths.SLSH}{folderPaths.DB_NAME}'

        if not os.path.exists(sqlite_file_path):
            con.create_connection(sqlite_file_path)

        assert sqlite_file_path != ""
        db_uri = f"sqlite:///{sqlite_file_path}"

    script_location = f'{folderPaths.BASEPATH_NETWORK}{folderPaths.SLSH}{"alembic"}'
    
    migrate = Migrate(script_location=script_location, uri=db_uri, is_sqlite=IS_SQLITE, db_file_path=sqlite_file_path, create_only_migration_file=CREATE_ONLY_MIGRATION_FILE, run_migration=RUN_MIGRATION, drop_alembic_stamp_head=DROP_ALEMBIC_TABLE_AND_STAMP_HEAD)
    if migrate.check_for_migrations():
        migrate.init_db()
    