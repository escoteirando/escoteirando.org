from sqlalchemy_serializer import SerializerMixin

from escoteirando.ext.database import db
from escoteirando.domain.enums import CodigoModalidade


class MAPPA_Grupo(db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo: int = db.Column(db.Integer, unique=True)
    codigoRegiao: str = db.Column(db.String(2))
    nome: str = db.Column(db.String(80))
    codigoModalidade: CodigoModalidade = db.Column(db.Enum(CodigoModalidade))

    """ Grupo Response
    [{
        "codigo":32,
        "codigoRegiao":"SC",
        "nome":"LEÕES DE BLUMENAU",
        "codigoModalidade":1
    }]
    """
