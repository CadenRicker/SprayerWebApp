from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import DevelopmentConfig, ProductionConfig, app_config
from flask_migrate import Migrate
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)
    from app import models
    return app
