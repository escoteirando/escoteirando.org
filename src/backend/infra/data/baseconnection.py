import pymongo
from infra.config import config

class BaseConnection:
    cursor = pymongo
    conn = pymongo.MongoClient(config.MONGODB_URL)
    db = conn[config.MONGODB_DB]
