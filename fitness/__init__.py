from fitness.blueprints import base, equipment, exercises, muscles, workouts
from fitness.database import database
from flask import Flask

def create_app(test_config = None):
  app = Flask(__name__, instance_relative_config = True)

  app.config.from_mapping(
    SECRET_KEY = 'dev'
  )

  if test_config is None: app.config.from_pyfile('config.py', silent = True)
  else: app.config.from_mapping(test_config)

  app.register_blueprint(base.bp)
  app.register_blueprint(equipment.bp)
  app.register_blueprint(exercises.bp)
  app.register_blueprint(muscles.bp)
  app.register_blueprint(workouts.bp)

  app.add_url_rule('/', endpoint = 'index')

  database.init_app(app)

  return app
