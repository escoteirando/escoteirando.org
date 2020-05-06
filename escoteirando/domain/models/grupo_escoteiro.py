from sqlalchemy_serializer import SerializerMixin

from escoteirando.domain.enums import CodigoModalidade
from escoteirando.ext.database import db


class GrupoEscoteiro(db.Model, SerializerMixin):
    __tablename__ = 'grupo_escoteiro'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo: int = db.Column(db.Integer, unique=True)
    codigo_regiao: str = db.Column(db.String(2))
    nome: str = db.Column(db.String(180))
    modalidade = db.Column(db.Enum(CodigoModalidade))
