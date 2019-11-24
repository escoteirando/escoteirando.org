# -*- coding: utf-8 -*-

# Python
from os import getenv
from os.path import join, dirname, isfile, realpath
import dotenv

# a partir do arquivo atual adicione ao path o arquivo .env
_ENV_FILE = join(dirname(__file__), '.env')

# existindo o arquivo faça a leitura do arquivo através da função load_dotenv
if not isfile(_ENV_FILE):
    _ENV_FILE = realpath(join(dirname(__file__), '..', '.env'))

if isfile(_ENV_FILE):
    dotenv.load_dotenv(dotenv_path=_ENV_FILE)


class Config:
    SECRET_KEY = getenv(
        'SECRET_KEY') or 'au0dj0ajsd0j30d9j0a9sjd0219jd0a9sjd0931jd09ajd09'
    APP_PORT = int(getenv('APP_PORT'))
    DEBUG = eval(getenv('DEBUG').title())
    MONGODB_URL = getenv('MONGODB_URL')
    MONGODB_DB = getenv("MONGODB_DB")
    CACHE_REPOSITORY = getenv("CACHE_REPOSITORY")
    MAPPA_BASE_URL = "http://mappa.escoteiros.org.br"
    MAPPA_ENABLED = getenv('MAPPA_ENABLED') == 'True'


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class DefaultConfig(Config):
    FLASK_ENV = 'production'


class TestConfig(Config):
    FLASK_ENV = 'testing'


configs = {
    'development': DevelopmentConfig,
    'default': DefaultConfig,
    'testing': TestConfig
}

config = configs[getenv('FLASK_ENV', 'development')]
