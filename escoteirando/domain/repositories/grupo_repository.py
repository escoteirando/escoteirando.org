from escoteirando.domain.models.db.grupo import Grupo

from .base_repository import BaseRepository


class GrupoRepository(BaseRepository):

    def load(self, codigo_grupo):
        return self.DB.session.query(Grupo).\
            filter(Grupo.codigo == codigo_grupo).first()

    def save(self, grupo: Grupo):
        _grupo = self.load(grupo.codigo)
        if _grupo:
            _grupo.id = grupo.id
            _grupo.codigo = grupo.codigo
            _grupo.cod_regiao = grupo.cod_regiao
            _grupo.nome = grupo.nome
            _grupo.cod_modalidade = grupo.cod_modalidade
        else:
            self.DB.session.add(_grupo)
