from sqlalchemy_serializer import SerializerMixin

from escoteirando.domain.enums import AreaDesenvolvimento, TipoAtividade
from escoteirando.ext.database import db


class Atividade(db.Model, SerializerMixin):

    __tablename__ = 'atividade'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    duracao: int = db.Column(db.Integer)
    tipo: TipoAtividade = db.Column(db.Enum(TipoAtividade))
    nome: str = db.Column(db.String(180))
    material: str = db.Column(db.Text())
    areas: AreaDesenvolvimento = db.Column(db.Enum(AreaDesenvolvimento))
    progressoes: str = db.Column(db.String(20))
    desenvolvimento: str = db.Column(db.Text())
