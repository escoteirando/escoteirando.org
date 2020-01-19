from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from .grupo_escoteiro import GrupoEscoteiro
from escoteirando.ext.database import db

class Encontro(db.Model, SerializerMixin):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grupo = relationship("GrupoEscoteiro")
