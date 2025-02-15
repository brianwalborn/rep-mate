from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from repmate.blueprints import base, equipment, exercises, muscles, workouts
from repmate.database import database
import os

def create_app(test_config = None):
  app = Flask(__name__, instance_relative_config = True)

  load_dotenv()

  app.config.from_mapping(
    SECRET_KEY = os.environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg://{os.environ.get('PGUSER')}:{os.environ.get('PGPASSWORD')}@{os.environ.get('PGHOST')}:{os.environ.get('PGPORT', '5432')}/{os.environ.get('PGDATABASE')}",
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  )

  if test_config is None: app.config.from_pyfile('config.py', silent = True)
  else: app.config.from_mapping(test_config)

  database.database.init_app(app)
  Migrate(app, database.database)

  app.register_blueprint(base.bp)
  app.register_blueprint(equipment.bp)
  app.register_blueprint(exercises.bp)
  app.register_blueprint(muscles.bp)
  app.register_blueprint(workouts.bp)

  app.add_url_rule('/', endpoint = 'index')

  return app
