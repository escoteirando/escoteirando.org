from flask_sqlalchemy import SQLAlchemy

from escoteirando.domain.models.mappa.secao import MAPPA_Secao
from escoteirando.mappa.models.secao_response import Secao
from escoteirando.domain.enums import TipoSecao


class ServiceSecao:

    def __init__(self, db):
        self.DB: SQLAlchemy = db

    def get_secao(self, codigo_secao) -> MAPPA_Secao:
        return self.DB.session.query(MAPPA_Secao).\
            filter(MAPPA_Secao.codigo == codigo_secao).first()

    def set_secao(self, secao: Secao):
        _secao = self.get_secao(secao.codigo)
        if not _secao:
            _secao = MAPPA_Secao()
            self.DB.session.add(_secao)

        _secao.codigo = secao.codigo
        _secao.codigoGrupo = secao.codigoGrupo
        _secao.codigoRegiao = secao.codigoRegiao
        _secao.codigoTipoSecao = TipoSecao(secao.codigoTipoSecao)
        _secao.nome = secao.nome
