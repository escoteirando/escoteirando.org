from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy_serializer import SerializerMixin

from escoteirando.ext.database import db


class Param(db.Model, SerializerMixin):
    """
    Parâmetro
    """

    __tablename__ = 'param'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer)
    param_name = db.Column(String(30))
    param_value = db.Column(String(180))
    last_update = db.Column(DateTime)
