from flask_sqlalchemy import SQLAlchemy

from escoteirando.domain.models.mappa.grupo import MAPPA_Grupo
from escoteirando.domain.enums import CodigoModalidade
from escoteirando.mappa.models.grupo_response import Grupo


class ServiceGrupo:

    def __init__(self, db):
        self.DB: SQLAlchemy = db

    def get_grupo(self, codigo_grupo):
        return self.DB.session.query(MAPPA_Grupo).\
            filter(MAPPA_Grupo.codigo == codigo_grupo).first()

    def set_grupo(self, _grupo: Grupo):
        grupo = self.get_grupo(_grupo.codigo)
        if not grupo:
            grupo = MAPPA_Grupo()
            self.DB.session.add(grupo)
        grupo.codigo = _grupo.codigo
        if isinstance(_grupo.codigoModalidade, int):
            _grupo.codigoModalidade = CodigoModalidade(_grupo.codigoModalidade)

        grupo.codigoModalidade = _grupo.codigoModalidade
        grupo.codigoRegiao = _grupo.codigoRegiao
        grupo.nome = _grupo.nome
