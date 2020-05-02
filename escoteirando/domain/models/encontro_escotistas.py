from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer
from sqlalchemy_serializer import SerializerMixin

from escoteirando.ext.database import db

from .encontro import Encontro
from .user import User


class EncontroEscotista(db.Model, SerializerMixin):
    """
    Referência ao escotista incluído no encontro
    """

    __tablename__ = 'encontro_escotista'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    encontro_id = db.Column(Integer, db.ForeignKey('encontro.id'))
    encontro = relationship("Encontro")
    escotista_id = db.Column(Integer, db.ForeignKey('user.id'))
    escotista = relationship("User")
