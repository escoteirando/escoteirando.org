from mongoengine import Document, IntField

from ..document_base_model import DocumentBaseModel


class Equipe(Document, DocumentBaseModel):
    codigo_equipe = IntField()
    # TODO: Itentificar modelagem da equipe

    def __dict__(self):
        return {
            "codigo_equipe": self.codigo_equipe
        }
