from escoteirando.ext.database import db
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))
    email = db.Column(db.String(140))

    # MAPPA fields
    user_id = db.Column(db.Integer, primary_key=True)
    codigo_associado = db.Column(db.Integer)
    user_name = db.Column(db.String(60))
    codigo_grupo = db.Column(db.Integer)
    codigo_regiao = db.Column(db.String(2))
