from mongoengine import (Document, IntField, ListField, ReferenceField,
                         StringField)

from domain.enums import AREAS_DESENVOLVIMENTO, TIPO_ATIVIDADE
from domain.models.me.progressao import Progressao


class Atividade(Document):
    duracao = IntField(min_value=1, required=True)
    tp_atividade = StringField(choices=TIPO_ATIVIDADE.keys(), required=True)
    ds_material = StringField()
    areas_desenvolvimento = ListField(
        StringField(choices=AREAS_DESENVOLVIMENTO.keys()))
    progressoes = ListField(ReferenceField(Progressao))
    ds_como_avaliar = StringField()
