from sqlalchemy_serializer import SerializerMixin

from escoteirando.domain.enums import TipoSecao
from escoteirando.ext.database import db

from ..dtos.base_dto import BaseDTO


class Secao(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo: int = db.Column(db.Integer, unique=True)
    nome: str = db.Column(db.String(80))
    cod_tipo_secao: TipoSecao = db.Column(db.Enum(TipoSecao))
    cod_grupo: int = db.Column(db.Integer)
    cod_regiao: str = db.Column(db.String(2))

    @staticmethod
    def from_dict(from_dict: dict):
        secao = Secao()
        dto = BaseDTO(from_dict)
        secao.codigo = dto.get('codigo', int)
        secao.nome = dto.get('nome', str)
        secao.cod_tipo_secao = dto.get('codigoTipoSecao', int)
        secao.cod_grupo = dto.get('codigoGrupo', int)
        secao.cod_regiao = dto.get('codigoRegiao', str)

        return secao

    @staticmethod
    def tipo_secao_str(tipo: TipoSecao):
        return {TipoSecao.ALCATEIA: "Alcatéia",
                TipoSecao.TROPA_ESCOTEIRA: "Tropa Escoteira",
                TipoSecao.TROPA_SENIOR: "Tropa Sênior",
                TipoSecao.CLA_PIONEIRO: "Clã Pioneiro"}[tipo]
