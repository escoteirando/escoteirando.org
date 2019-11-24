from mongoengine import DateField, Document, ReferenceField, StringField, ListField

from domain.models.ue.associado import Associado
from domain.models.ue.sessao import Sessao


class Reuniao(Document):
    sessao = ReferenceField(Sessao, required=True)
    dt_reuniao = DateField(required=True)
    ds_rec_materiais = StringField()
    ds_rec_humanos = ListField(ReferenceField(Associado))
    ds_preparacao = StringField()
    
