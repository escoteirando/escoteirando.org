from flask import Flask
from .config import config

def create_app(config_name):
    app = Flask('escoteirando')
    app.config.from_object(config[config_name])
    return app
    