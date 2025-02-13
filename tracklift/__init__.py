from flask import Flask
from flask_migrate import Migrate
from tracklift.blueprints import base, equipment, exercises, muscles, workouts
from tracklift.database import database
import os

def create_app(test_config = None):
  app = Flask(__name__, instance_relative_config = True)

  app.config.from_mapping(
    SECRET_KEY = os.environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg://tracklift:irjcoYW3J8mCzrRjCNop@localhost:5432/tracklift",
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  )

  if test_config is None: app.config.from_pyfile('config.py', silent = True)
  else: app.config.from_mapping(test_config)

  database.database.init_app(app)
  Migrate(app, database.database)
  database.register_commands(app)

  app.register_blueprint(base.bp)
  app.register_blueprint(equipment.bp)
  app.register_blueprint(exercises.bp)
  app.register_blueprint(muscles.bp)
  app.register_blueprint(workouts.bp)

  app.add_url_rule('/', endpoint = 'index')

  return app
