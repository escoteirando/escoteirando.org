from flask_mongoengine import MongoEngine, create_connections
from mongoengine.connection import get_connection, _connections
from pymongo.uri_parser import parse_uri
from infra.config import config


class BaseConnection:

    def __init__(self):
        if len(_connections) == 0:
            ms = parse_uri(config.MONGODB_URL)
            mongo_settings = {
                "db": config.MONGODB_DB,
                "host": ms['nodelist'][0][0],
                "port": ms['nodelist'][0][1]
            }
            create_connections(mongo_settings)
