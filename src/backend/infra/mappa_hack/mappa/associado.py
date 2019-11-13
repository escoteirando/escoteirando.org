from .basemodel import BaseModel


class Associado(BaseModel):

    def __init__(self, content):
        super().__init__(content)
        [self.codigo, self.nome, self.codigoFoto, self.codigoEquipe, self.username, self.numeroDigito, self.dataNascimento, self.dataValidade, self.nomeAbreviado, self.sexo, self.codigoRamo,
         self.codigoCategoria, self.codigoSegundaCategoria, self.codigoTerceiraCategoria, self.linhaFormacao,
         self.codigoRamoAdulto, self.dataAcompanhamento] = self.get([
             'codigo', 'nome', 'codigoFoto', 'codigoEquipe', 'username', 'numeroDigito', 'dataNascimento', 'dataValidade',
             'nomeAbreviado', 'sexo', 'codigoRamo', 'codigoCategoria', "codigoSegundaCategoria", "codigoTerceiraCategoria", "linhaFormacao",
             "codigoRamoAdulto", "dataAcompanhamento"
         ])

        # {"codigo":850829,"nome":"GUIONARDO FURLAN","codigoFoto":null,"codigoEquipe":null,
        # "username":1247937,"numeroDigito":3,"dataNascimento":"Sat Feb 05 1977 00:00:00 GMT+0000 (UTC)",
        # "dataValidade":"2019-01-01T00:00:00.000Z","nomeAbreviado":"","sexo":"M","codigoRamo":2,
        # "codigoCategoria":5,"codigoSegundaCategoria":0,"codigoTerceiraCategoria":0,"linhaFormacao":"Escotista",
        # "codigoRamoAdulto":2,"dataAcompanhamento":null}
