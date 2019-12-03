""" Clustersitter """
__author__ = "titus"

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from loguru import logger
from config import Config

logger.add(
    "logs.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message} ",
    level=30
)

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(Config())
    app.app_context().push()

    db.init_app(app)
    db.create_all()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app = create_app('default')