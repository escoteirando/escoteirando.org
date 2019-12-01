from logging import Logger

from flask_mongoengine import create_connections
from pymongo.uri_parser import parse_uri

from infra.config import config
from infra.log import getLogger

logger = getLogger('mongodb')

_connected = False


class BaseConnection:

    def __init__(self):
        global _connected
        if not _connected:
            ms = parse_uri(config.MONGODB_URL)
            mongo_settings = {
                "db": config.MONGODB_DB,
                "host": ms['nodelist'][0][0],
                "port": ms['nodelist'][0][1]
            }
            create_connections(mongo_settings)
            _connected = True

    @property
    def logger(self) -> Logger:
        return logger
