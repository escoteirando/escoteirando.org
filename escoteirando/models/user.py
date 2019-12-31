from escoteirando.ext.database import db
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))
    ''' Email of user '''
    email = db.Column(db.String(140))
    verified = db.Column(db.Boolean)

    # MAPPA fields
    user_id = db.Column(db.Integer, primary_key=True)
    codigo_associado = db.Column(db.Integer)
    codigo_grupo = db.Column(db.Integer)
    codigo_regiao = db.Column(db.String(2))
