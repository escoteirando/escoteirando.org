
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
