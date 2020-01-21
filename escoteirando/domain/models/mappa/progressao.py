from sqlalchemy_serializer import SerializerMixin

from escoteirando.domain.enums import TipoSecao
from escoteirando.ext.database import db


class MAPPA_Progressao(db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo: int = db.Column(db.Integer, unique=True)
    descricao: str = db.Column(db.String(180))
    codigoUeb: str = db.Column(db.String(4))
    ordenacao: int = db.Column(db.Integer)
    codigoCaminho: int = db.Column(db.Integer)
    codigoDesenvolvimento: int = db.Column(db.Integer)
    codigoCompetencia: int = db.Column(db.Integer)
    segmento: str = db.Column(db.String(60))
    ramo: TipoSecao = db.Column(db.Enum(TipoSecao))

    """ Progressao Response
    {
        "codigo": 1,
        "descricao": "Ouvir o episódio \"Irmãos de Mowgli\" do Livro da Selva.",
        "codigoUeb": "S2",
        "ordenacao": 2,
        "codigoCaminho": 1,
        "codigoDesenvolvimento": 23,
        "numeroGrupo": null,
        "codigoRegiao": null,
        "codigoCompetencia": 38,
        "segmento": "PROMESSA_ESCOTEIRA_LOBINHO"
    }
    """
