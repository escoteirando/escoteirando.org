from escoteirando.domain.models.db.secao import Secao

from .base_repository import BaseRepository


class SecaoRepository(BaseRepository):

    def load(self, codigo: int) -> Secao:
        return self.DB.session.query(Secao).\
            filter(Secao.codigo == codigo).first()

    def save(self, secao: Secao):
        _secao = self.load(secao.codigo)
        if _secao:
            _secao.codigo = secao.codigo
            _secao.cod_grupo = secao.cod_grupo
            _secao.cod_regiao = secao.cod_regiao
            _secao.cod_tipo_secao = secao.cod_tipo_secao
            _secao.nome = secao.nome
        else:
            self.DB.session.add(_secao)
