# -*- coding: utf-8 -*-

# Python
from os import getenv

import dotenv

dotenv.load_dotenv(verbose=True)


def _getenv(key: str, default: str = ""):
    value = getenv(key, None)
    if isinstance(default, bool):
        value = value.upper() == 'TRUE'
    elif isinstance(default, int):
        value = int(value)

    return value


DEFAULT_SECRET_KEY = 'Escoteirando_Secret_Key'


class Config:
    SECRET_KEY = _getenv('SECRET_KEY', DEFAULT_SECRET_KEY)
    APP_PORT = _getenv('APP_PORT', 5000)
    DEBUG = _getenv('DEBUG', True)
    MONGODB_URL = _getenv('MONGODB_URL')
    MONGODB_DB = _getenv("MONGODB_DB", '')
    CACHE_REPOSITORY = _getenv("CACHE_REPOSITORY")
    MAPPA_BASE_URL = _getenv(
        "MAPPA_BASE_URL", "http://mappa.escoteiros.org.br")
    MAPPA_ENABLED = _getenv('MAPPA_ENABLED', True)


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

config: Config = configs[getenv('FLASK_ENV', 'development')]
