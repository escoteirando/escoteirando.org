""" MAPPA MODEL: Associado
{
    "codigo":850829,
    "nome":"GUIONARDO FURLAN",
    "codigoFoto":null,
    "codigoEquipe":null,
    "username":1247937,
    "numeroDigito":3,
    "dataNascimento":"Sat Feb 05 1977 00:00:00 GMT+0000 (UTC)",
    "dataValidade":"2019-01-01T00:00:00.000Z",
    "nomeAbreviado":"",
    "sexo":"M",
    "codigoRamo":2,
    "codigoCategoria":5,
    "codigoSegundaCategoria":0,
    "codigoTerceiraCategoria":0,
    "linhaFormacao":"Escotista",
    "codigoRamoAdulto":2,
    "dataAcompanhamento":null
}
"""
from flask_mongoengine import Document
from mongoengine import DateField, IntField, ReferenceField, StringField

from ..document_base_model import DocumentBaseModel
from .equipe import Equipe


class Associado(Document, DocumentBaseModel):
    '''
    Associado

    codigo: int (*)

    ds_nome: str (*)

    nr_registro: int (*)

    dt_nascimento: datetime

    tp_sexo: str

    equipe: Equipe

    '''
    codigo = IntField(unique=True)
    ds_nome = StringField(required=True)
    nr_registro = IntField(required=True)
    dt_nascimento = DateField()
    tp_sexo = StringField()
    equipe = ReferenceField(Equipe)

    def __dict__(self):
        return {
            "codigo": self.codigo,
            "ds_nome": self.ds_nome,
            "nr_registro": self.nr_registro,
            "dt_nascimento": self.dt_nascimento,
            "tp_sexo": self.tp_sexo,
            "equipe": None if self.equipe is None else self.equipe.__dict__()
        }

    def _after_from_dict(self):
        self.equipe = Equipe().from_dict(self.equipe)
