
import logging

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()


def init_app(app):
    db.init_app(app)
    app.db = db
    migrate.init_app(app, db)
    logging.basicConfig()   # log messages to stdout
    logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.INFO)
