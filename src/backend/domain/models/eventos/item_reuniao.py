from mongoengine import Document, IntField, ReferenceField, StringField

from domain.models.eventos.atividade import Atividade
from domain.models.ue.associado import Associado


class ItemReuniao(Document):
    atividade = ReferenceField(Atividade, required=True)
    duracao = IntField(min_value=1)
    responsavel = ReferenceField(Associado)
    ordem = IntField(min_value=1, required=True)
    ds_obs = StringField()
