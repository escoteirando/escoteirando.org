from mongoengine import IntField
from flask_mongoengine import Document

from ..document_base_model import DocumentBaseModel


class Equipe(Document, DocumentBaseModel):
    codigo_equipe = IntField(required=True)
    # TODO: Itentificar modelagem da equipe

    def __dict__(self):
        return {
            "codigo_equipe": self.codigo_equipe
        }
