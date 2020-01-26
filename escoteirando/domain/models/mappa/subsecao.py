from sqlalchemy_serializer import SerializerMixin

from escoteirando.ext.database import db


class MAPPA_SubSecao(db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo: int = db.Column(db.Integer, unique=True)
    nome: str = db.Column(db.String(80))
    codigoSecao: int = db.Column(db.Integer)
    id_lider: int = db.Column(db.Integer)
    id_sublider: int = db.Column(db.Integer)
    # TODO: Modelar Subsecao para incluir associados
