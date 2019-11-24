from os import getenv
from os.path import dirname, isfile, join, realpath


from flask import Flask, request
from flask_mongoengine import MongoEngine
from pymongo import uri_parser
from app.api.controllers import api
from app.auth.controllers import auth
from app.main.controllers import main
from app.mappa.controllers import mappa
from infra.config import config
from infra.log import getLogger
from infra.tools.networking import test_mongodb, test_tcp_port

logger = getLogger("app")

if not test_mongodb(config.MONGODB_URL):
    logger.error("MONGODB UNAVAILABLE")
    raise ConnectionError("MONGODB UNAVAILABLE")


logger.info("app init")


def create_app(config_name):
    logger.info(f'app[{config_name}]')
    global config
    ms = uri_parser.parse_uri(config.MONGODB_URL)
    mongo_settings = {
        "db": config.MONGODB_DB,
        "host": ms['nodelist'][0][0],
        "port": ms['nodelist'][0][1]
    }
    if ms['password']:
        mongo_settings['password'] = ms['password']
    if ms['username']:
        mongo_settings['username'] = ms['username']

    app = Flask('escoteirando')
    app.config.from_object(config)
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(mappa, url_prefix='/mappa')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/auth')
    app.config['MONGODB_SETTINGS'] = mongo_settings

    db = MongoEngine()
    db.init_app(app)
    from domain.models.user import check_admin
    check_admin()
    return app


# instancia nossa função factory criada anteriormente
app = create_app(getenv('FLASK_ENV') or 'development')


# @app.before_request
# def global_before_request():
#app.logger.info("Global before request")
