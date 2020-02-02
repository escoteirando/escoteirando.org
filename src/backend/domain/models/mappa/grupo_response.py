from ..basemodel import BaseModel

class Grupo(BaseModel):
    """ Grupo Response
    [{
        "codigo":32,
        "codigoRegiao":"SC",
        "nome":"LEÕES DE BLUMENAU",
        "codigoModalidade":1
    }]
    """

    def __init__(self, fromDict):
        self.codigo = None
        self.codigoRegiao=None
        self.nome=None
        self.codigoModalidade=None

        if(isinstance(fromDict,list)):
            if len(fromDict)>0:
                fromDict=fromDict[0]
            else:
                raise Exception('Grupo constructor fromDict invalid')

        super().__init__(fromDict)
