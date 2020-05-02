from escoteirando.domain.models.db.associado import Associado

from .base_repository import BaseRepository


class AssociadoRepository(BaseRepository):

    def load(self, codigo: int) -> Associado:
        return self.DB.session.query(Associado).\
            filter(Associado.codigo == codigo).first()

    def save(self, associado: Associado):
        _associado = self.load(associado.codigo)
        if _associado:
            _associado.codigo = associado.codigo
            _associado.cod_categoria = associado.cod_categoria
            _associado.cod_equipe = associado.cod_equipe
            _associado.cod_foto = associado.cod_foto
            _associado.cod_ramo = associado.cod_ramo
            _associado.cod_ramo_adulto = associado.cod_ramo_adulto
            _associado.cod_segunda_categoria = associado.cod_segunda_categoria
            _associado.cod_terceira_categoria = associado.cod_terceira_categoria
            _associado.dt_nascimento = associado.dt_nascimento
            _associado.dt_validade = associado.dt_validade
            _associado.linha_formacao = associado.linha_formacao
            _associado.nome = associado.nome
            _associado.nome_abreviado = associado.nome_abreviado
            _associado.numero_digito = associado.numero_digito
            _associado.sexo = associado.sexo
            _associado.username = associado.username
        else:
            self.DB.session.add(_associado)
