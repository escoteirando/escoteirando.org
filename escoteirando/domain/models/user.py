from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash

from escoteirando.ext.database import db


class User(db.Model, SerializerMixin, UserMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))
    ''' Email of user '''
    email = db.Column(db.String(140))
    verified = db.Column(db.Boolean)
    sexo = db.Column(db.String(1))

    # MAPPA fields
    user_id = db.Column(db.Integer)
    codigo_associado = db.Column(db.Integer)
    codigo_grupo = db.Column(db.Integer)
    codigo_regiao = db.Column(db.String(2))

    @property
    def is_active(self):
        return self.verified
