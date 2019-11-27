from mongoengine import IntField, LazyReferenceField, StringField
from flask_mongoengine import Document
from werkzeug.security import generate_password_hash

from domain.enums import USER_LEVELS
from domain.models.ue.associado import Associado

from .document_base_model import DocumentBaseModel


def check_admin():
    _admin: User = User.objects(user_name='admin')[0:1]

    if len(_admin) == 0:
        User(user_name='admin', password=generate_password_hash(
            'admin'), level=2).save()
    else:
        _admin = _admin[0]

    for ass in Associado.objects(codigo=850829):
        assoc = ass
    if not assoc:
        assoc = Associado(
            codigo=850829,
            ds_nome="GUIONARDO FURLAN",
            nr_registro=1,
            dt_nascimento="1977-02-05",
            tp_sexo="M")
        assoc.save()

    _admin.update(set__associado=assoc)

    del(_admin)


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
