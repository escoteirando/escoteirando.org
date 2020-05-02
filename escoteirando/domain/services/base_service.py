from cache_gs import CacheGS
from flask_sqlalchemy import SQLAlchemy

from escoteirando.ext.configs import Configs
from escoteirando.ext.logging import get_logger


class BaseService:

    def __init__(self, db):
        self.configs = Configs.Instance()
        self.cache = CacheGS(self.configs.CACHE_STRING_CONNECTION)

        self.DB: SQLAlchemy = db
        self.log = get_logger()
