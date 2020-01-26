from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer
from sqlalchemy_serializer import SerializerMixin

from escoteirando.ext.database import db


class EncontroAtividade(db.Model, SerializerMixin):
    """
    Referência ao escotista incluído no encontro
    """

    __tablename__ = 'encontro_atividade'

    id = db.Column(Integer, primary_key=True, autoincrement=True)

    encontro_id = db.Column(Integer, db.ForeignKey('encontro.id'))
    encontro = relationship("Encontro")
    atividade_id = db.Column(Integer, db.ForeignKey('atividade.id'))
    atividade = relationship("Atividade")
    duracao: int = db.Column(Integer)
    ordem: int = db.Column(Integer)
