from flask import current_app, g
from flask.cli import with_appcontext
import click
import os
import psycopg
import psycopg.rows

def close_database(e = None) -> None:
  database = g.pop('database', None)

  if database is not None:
    database.close()

def get_connection() -> psycopg.Connection:
  if 'database' not in g:
    host = os.environ.get('PGHOST', 'localhost')
    database = os.environ.get('PGDATABASE', 'fitness')
    user = os.environ.get('PGUSER', 'fitness')
    password = os.environ.get('PGPASSWORD', 'irjcoYW3J8mCzrRjCNop')
    g.database = psycopg.connect(f'host={host} dbname={database} user={user} password={password}')

  return g.database

def init_app(app) -> None:
  app.teardown_appcontext(close_database)
  app.cli.add_command(init_database_command)

def init_database() -> None:
  connection = get_connection()

  with current_app.open_resource('database/schema.sql') as f:
    cursor = connection.cursor()
    cursor.execute(f.read().decode('utf8'))
    connection.commit()
    cursor.close()

  connection.close()

@click.command('init-database')
@with_appcontext
def init_database_command() -> None:
    init_database()

    click.echo('Initialized the database.')
