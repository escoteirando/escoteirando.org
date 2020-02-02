""" MAPPA MODEL: Equipe

# TODO: Itentificar modelagem da equipe

"""
from flask_mongoengine import Document
from mongoengine import IntField

from ..document_base_model import DocumentBaseModel


class Equipe(Document, DocumentBaseModel):
    codigo_equipe = IntField(required=True)

    def __dict__(self):
        return {
            "codigo_equipe": self.codigo_equipe
        }
