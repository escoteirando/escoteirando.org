from flask_login import UserMixin
from sqlalchemy import Column
from sqlalchemy.types import Boolean, Date, Integer, String
from sqlalchemy_serializer import SerializerMixin

from escoteirando.ext.database import db


class User(db.Model, SerializerMixin, UserMixin):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(140))
    password = Column(String(512))
    ''' Email of user '''
    email = Column(String(140))
    verified_email = Column(Boolean())
    sexo = Column(String(1))
    # MAPPA fields
    user_id = Column(Integer)
    user_name = Column(String(40))
    codigo_associado = Column(Integer)
    nome = Column(String(140))
    codigo_grupo = Column(Integer)
    nome_grupo = Column(String(140))
    codigo_regiao = Column(String(2))
    codigo_secao = Column(Integer)
    authorization = Column(String(64))
    auth_valid_until = Column(Integer, default=0)
    data_nascimento = Column(Date)
    ativo = Column(Boolean(), default=True)

    @property
    def is_active(self):
        return self.ativo
