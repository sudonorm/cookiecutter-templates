## sqlalchemy_database
This cookiecutter template can be used to create a database workflow which is managed using `SQLAlchemy` with database migrations and schema changes being done by `alembic` in a fluid way which automatically checks for database revisions and automatically executes the migrations if any changes are found. There's also the option to either spin up a SQLite database for quick tests or to use an actual database e.g. postgres, MySQL. The cookiecutter template will need to be extended with the appropriate crud functions on a use-case basis.

## Usage:
- Change the paths in the `resources/folderPaths` file.
- Modify the Tables in the `db/dataModel.py` file.
- Run the `db/dataModel.py` file or `db/init_or_update_db.py` file to initialize the database.