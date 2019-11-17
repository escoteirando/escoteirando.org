from os import getenv
from os.path import dirname, isfile, join, realpath

import dotenv
from flask import Flask

from app.api.controllers import api
from app.main.controllers import main
from app.mappa.controllers import mappa
from infra.config import configs
from infra.log import logging

logging.info("app init")


def create_app(config_name):
    logging.info(f'app[{config_name}]')
    app = Flask('escoteirando')
    app.config.from_object(configs[config_name])
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(mappa, url_prefix='/mappa')
    app.register_blueprint(api, url_prefix='/api')
    return app


# a partir do arquivo atual adicione ao path o arquivo .env
_ENV_FILE = join(dirname(__file__), '.env')

# existindo o arquivo faça a leitura do arquivo através da função load_dotenv
if not isfile(_ENV_FILE):
    _ENV_FILE = realpath(join(dirname(__file__), '..', '.env'))

if isfile(_ENV_FILE):
    logging.info(f'ENV FILE: {_ENV_FILE}')
    dotenv.load_dotenv(dotenv_path=_ENV_FILE)

# instancia nossa função factory criada anteriormente
app = create_app(getenv('FLASK_ENV') or 'default')
