# About

This repo is a culmination of cookiecutter templates for doing various things. Each cookiecutter template is organized into the following directories:

## sqlalchemy_database

This cookiecutter template can be used to create a database workflow which is managed using `SQLAlchemy` with database migrations and schema changes being done by `alembic` in a fluid way which automatically checks for database revisions and automatically executes the migrations if any changes are found. There's also the option to either spin up a SQLite database for quick tests or to use an actual database e.g. postgres, MySQL. The cookiecutter template will need to be extended with the appropriate crud functions on a use-case basis.

    cookiecutter https://github.com/sudonorm/cookiecutter-templates.git --directory="sqlalchemy_database"

## Simple dash app

This is a cookiecutter template which can be used to create a dash application that can be run in a docker container.

    cookiecutter https://github.com/sudonorm/cookiecutter-templates.git --directory="simple_dash_app"
