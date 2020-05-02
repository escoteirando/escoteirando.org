from flask_sqlalchemy import SQLAlchemy

from escoteirando.ext.logging import get_logger


class BaseRepository:

    LOG = get_logger()

    def __init__(self, db):
        if not isinstance(db, SQLAlchemy):
            raise RepositoryException('%s: db is not SQLAlchemy instance [%s]',
                                      self.__class__,
                                      db)
        self.DB: SQLAlchemy = db

    def save(self, data):
        raise NotImplementedError("save")

    def load(self, key):
        raise NotImplementedError("load")

    def delete(self, key):
        raise NotImplementedError("delete")


class RepositoryException(Exception):
    pass
