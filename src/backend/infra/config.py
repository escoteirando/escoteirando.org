# -*- coding: utf-8 -*-

# Python
from os import getenv


class Config:
    SECRET_KEY = getenv(
        'SECRET_KEY') or 'au0dj0ajsd0j30d9j0a9sjd0219jd0a9sjd0931jd09ajd09'
    APP_PORT = int(getenv('APP_PORT'))
    DEBUG = eval(getenv('DEBUG').title())
    MONGODB_HOST = getenv('MONGODB_HOST')
    MONGODB_DB = getenv("MONGODB_DB")
    CACHE = getenv("CACHE_REPOSITORY")


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class DefaultConfig(Config):
    FLASK_ENV = 'production'


configs = {
    'development': DevelopmentConfig,
    'default': DefaultConfig,
    'testing': DevelopmentConfig
}

config = configs[getenv('FLASK_ENV', 'development')]
