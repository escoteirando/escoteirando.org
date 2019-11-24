from mongoengine import (Document, IntField, ListField, ReferenceField,
                         StringField)

from .associado import Associado
from .sessao import Sessao


class Subsessao(Document):
    sessao = ReferenceField(Sessao, required=True)
    ds_nome = StringField(required=True)
    as_lider = ReferenceField(Associado)
    as_vicelider = ReferenceField(Associado)
    associados = ListField(ReferenceField(Associado))
