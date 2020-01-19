from flask_sqlalchemy import SQLAlchemy

from escoteirando.domain.enums import TipoSecao
from escoteirando.domain.models.mappa import MAPPA_Progressao


class ServiceProgressoes:

    def __init__(self, db: SQLAlchemy):
        self.DB: SQLAlchemy = db

    def get_progressoes(self, ramo: TipoSecao):
        return self.DB.session.query(MAPPA_Progressao).filter(MAPPA_Progressao.ramo == ramo).all()

    def update_progressoes(self, progressoes: list):
        for progressao in progressoes:
            assert isinstance(progressao, MAPPA_Progressao), \
                'item is not of type MAPPA_Progressao'
        self.DB.session.bulk_save_objects(progressoes)
        self.DB.session.commit()
