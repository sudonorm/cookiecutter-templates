import alembic
from alembic.config import CommandLine
import sqlite3
import re
import os
import sys
from alembic.config import Config
from alembic import command
from typing import Any
home_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(home_dir)
from resources import folderPaths
import os
import time
import sys

class Connection:

    def create_connection(self, db_file):
            """ create a database connection to a SQLite database """
            conn = None
            try:
                conn = sqlite3.connect(db_file)
            except sqlite3.Error as e:
                print(e)
            finally:
                if conn:
                    conn.close()

class Migrate(Connection):

    def __init__(self, script_location: str, uri: str, is_sqlite:bool = False, db_file_path:str = None, run_only_migration:bool = False) -> None:
        self.script_location = script_location
        self.uri = uri
        self.is_sqlite = is_sqlite
        self.db_file_path = db_file_path
        self.run_only_migration = run_only_migration

    def init_db(self) -> None:

        if self.is_sqlite:
            if not os.path.exists(self.db_file_path):
                self.create_connection(self.db_file_path)

        has_changes = self.check_for_migrations()

        if not 'alembic' in sys.modules['__main__'].__file__:
            if has_changes:
                if not self.run_only_migration:
                    self.create_migrations(f'{time.strftime("%Y%m%d", time.gmtime())}{" migration"}')
                self.run_migrations()

    def check_for_migrations(self) -> bool:
        config = Config()
        config.set_main_option("sqlalchemy.url", self.uri)
        config.set_main_option('script_location', self.script_location)

        try:
            command.check(config)
            return False
        except:
            return True

    def has_db_revisions(self, path_to_file:str)  -> bool:
        with open(path_to_file) as f:
            contents = f.read()

        # Define regular expressions to match the entire function bodies
        upgrade_pattern = re.compile(r'def upgrade\(\).*?^\s*# ### end Alembic commands ###', re.MULTILINE | re.DOTALL)
        downgrade_pattern = re.compile(r'def downgrade\(\).*?^\s*# ### end Alembic commands ###', re.MULTILINE | re.DOTALL)

        # Use the regular expressions to extract the function bodies from the file contents
        upgrade_match = upgrade_pattern.search(contents)
        downgrade_match = downgrade_pattern.search(contents)

        if upgrade_match and downgrade_match:
            upgrade_body = upgrade_match.group(0)
            downgrade_body = downgrade_match.group(0)

            if 'pass' not in upgrade_body and 'pass' not in downgrade_body:
                print("Both functions contain code other than 'pass'.")
                return True
            else:
                print("At least one function contains only 'pass'.")
                return False
        else:
            print("Could not find both functions in the file.")
            return False
        
    def create_migrations(self, message:str) -> None:
        namespace_revision = CommandLine().parser.parse_args(["revision", "--autogenerate"])
        config = Config(cmd_opts=namespace_revision)
        config.set_main_option("sqlalchemy.url", self.uri)
        config.set_main_option('script_location', self.script_location)
        command.revision(config, message=message, autogenerate=True)

    def run_migrations(self) -> None:
        # namespace_revision = CommandLine().parser.parse_args(["upgrade", "head"])
        config = Config()
        config.set_main_option("sqlalchemy.url", self.uri)
        config.set_main_option('script_location', self.script_location)
        command.upgrade(config, 'head')
