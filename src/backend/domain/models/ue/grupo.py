from mongoengine import Document, IntField, StringField, ReferenceField, ListField
from .sessao import Sessao


class Grupo(Document):
    """
    Grupo Escoteiro
    """

    nr_grupo = IntField(required=True, min_value=1,
                        max_value=999, unique=True, primary_key=True)
    ds_nome = StringField(required=True)
    cd_regiao = StringField(required=True, min_length=2, max_length=2)
    sessoes = ListField(ReferenceField(Sessao))
