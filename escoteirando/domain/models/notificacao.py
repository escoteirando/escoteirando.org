from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin

from escoteirando.ext.database import db


class Notificacao(db.Model, SerializerMixin):
    __tablename__ = 'notificacao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario: int = Column(Integer)
    data_notificacao: datetime = Column(DateTime(timezone=True))
    mensagem: str = Column(String(180))
    valida_ate: datetime = Column(DateTime(timezone=True))
    link: str = Column(String(240))
