from mongoengine import Document, ReferenceField, IntField, StringField, ListField
from .grupo import Grupo


class Sessao(Document):
    grupo = ReferenceField(Grupo, required=True)
    id_sessao = IntField(min_value=1, max_value=999999, required=True)
    tp_sessao = IntField(required=True)
    ds_nome = StringField(required=True)
