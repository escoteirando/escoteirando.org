from flask_mongoengine import Document
from mongoengine import IntField, LazyReferenceField, StringField

from domain.enums import USER_LEVELS
from domain.models.ue.associado import Associado

from .document_base_model import DocumentBaseModel


class User(Document, DocumentBaseModel):
    """
    User class

    user_name = mappa

    associado (Associado)

    password

    level
    """

    user_name = StringField(unique=True)
    associado = LazyReferenceField(Associado, dbref=True, default=None)
    password = StringField(required=True)
    level = IntField(required=True, choices=USER_LEVELS.keys())

    def __dict__(self):
        return{
            "user_name": self.user_name,
            "associado": self.getDict(self.associado),
            "password": self.password,
            "level": self.level
        }

    def _after_from_dict(self):
        self.associado = Associado().from_dict(self.associado)
