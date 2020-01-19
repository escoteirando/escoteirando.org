from escoteirando.ext.database import db
from sqlalchemy_serializer import SerializerMixin
from escoteirando.domain.enums import AreaDesenvolvimento


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    price = db.Column(db.Numeric())
    description = db.Column(db.Text)
    area = db.Column(db.Enum(AreaDesenvolvimento))
