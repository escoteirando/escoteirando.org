from flask_sqlalchemy import SQLAlchemy

from escoteirando.domain.models.mappa.subsecao import MAPPA_SubSecao
from escoteirando.mappa.models.subsecao_response import Subsecao


class ServiceSubSecao:

    def __init__(self, db):
        self.DB: SQLAlchemy = db

    def get_subsecao(self, codigo_secao, codigo_subsecao) -> MAPPA_SubSecao:
        return self.DB.session.query(MAPPA_SubSecao).\
            filter(MAPPA_SubSecao.codigo ==
                   codigo_subsecao and
                   MAPPA_SubSecao.codigoSecao == codigo_secao).first()

    def set_secao(self, subsecao: Subsecao):
        _secao = self.get_secao(subsecao.codigoSecao, subsecao.codigo)
        if not _secao:
            _secao = MAPPA_SubSecao()
            self.DB.session.add(_secao)

        _secao.codigo = subsecao.codigo
        _secao.codigoSecao = subsecao.codigoSecao
        _secao.id_lider = subsecao.codigoLider
        _secao.id_sublider = subsecao.codigoViceLider
        _secao.nome = subsecao.nome
