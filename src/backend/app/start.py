from infra.config import config
from infra.tools.networking import test_tcp_port

from flask import Flask
from flask_mongoengine import MongoEngine
from . import logger


app: Flask = None


def create_app(config_name):
    logger.info(f'app[{config_name}]')

    from app.api.controllers import api
    from app.auth.controllers import auth
    from app.main.controllers import main
    from app.mappa.controllers import mappa

    global app
    app = Flask('escoteirando')

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(mappa, url_prefix='/mappa')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/auth')

    db = MongoEngine()
    db.init_app(app)

    return app


def pre_run_tasks():
    logger.info('Pre-run tasks')
    logger.info(' - Checking database [{0}:{1}]'
                .format(config.MONGODB_HOST, config.MONGODB_PORT))
    if not test_tcp_port(config.MONGODB_HOST, config.MONGODB_PORT):
        logger.error(' [!] DATABASE UNAVAILABLE')
        return False

    return True
