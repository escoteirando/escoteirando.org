from .basemodel import BaseModel

class Associado(BaseModel):
    """ Associado Response
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

    def __init__(self,fromDict):
        self.codigo = None
        self.nome=None
        self.codigoFoto=None
        self.codigoEquipe=None
        self.username=None
        self.numeroDigito=None
        self.dataNascimento = None
        self.dataValidade=None
        self.nomeAbreviado=None
        self.sexo=None
        self.codigoRamo=None
        self.codigoCategoria=None
        self.codigoSegundaCategoria=None
        self.codigoTerceiraCategoria=None
        self.linhaFormacao=None
        self.codigoRamoAdulto=None
        self.dataAcompanhamento=None
        super().__init__(fromDict)




      