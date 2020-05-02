from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, DateTime, Integer, Text
from sqlalchemy_serializer import SerializerMixin

from escoteirando.ext.database import db

from .grupo_escoteiro import GrupoEscoteiro


class Encontro(db.Model, SerializerMixin):

    __tablename__ = 'encontro'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    grupo_id = db.Column(Integer, db.ForeignKey('grupo_escoteiro.id'))
    grupo = relationship("GrupoEscoteiro")
    inicio = db.Column(DateTime)
    termino = db.Column(DateTime)
    recursos_materiais = db.Column(Text)
    preparacao_previa = db.Column(Text)
    publicado = db.Column(Boolean, default=False)
