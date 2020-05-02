
from sqlalchemy_serializer import SerializerMixin

from escoteirando.domain.enums import CodigoModalidade
from escoteirando.ext.database import db

from ..dtos.base_dto import BaseDTO


class Grupo(db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo: int = db.Column(db.Integer, unique=True)
    cod_regiao: str = db.Column(db.String(2))
    nome: str = db.Column(db.String(80))
    cod_modalidade: CodigoModalidade = db.Column(db.Enum(CodigoModalidade))

    @staticmethod
    def from_dict(from_dict: dict):
        grupo = Grupo()
        dto = BaseDTO(from_dict)
        grupo.codigo = dto.get('codigo', int)
        grupo.cod_modalidade = dto.get('codigoModalidade', int)
        grupo.nome = dto.get('nome', str)
        grupo.cod_regiao = dto.get('codigoRegiao', str)

        return grupo
