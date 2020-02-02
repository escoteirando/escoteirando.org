from sqlalchemy_serializer import SerializerMixin

from escoteirando.domain.enums import TipoSecao
from escoteirando.ext.database import db


class MAPPA_Secao(db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo: int = db.Column(db.Integer, unique=True)
    nome: str = db.Column(db.String(80))
    codigoTipoSecao: TipoSecao = db.Column(db.Enum(TipoSecao))
    codigoGrupo: int = db.Column(db.Integer)
    codigoRegiao: str = db.Column(db.String(2))
