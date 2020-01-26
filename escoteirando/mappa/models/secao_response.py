from .basemodel import BaseModel


class Secao(BaseModel):

    def __init__(self, fromDict):
        self.codigo = None
        self.nome = None
        self.codigoTipoSecao = None
        self.codigoGrupo = None
        self.codigoRegiao = None

        if(isinstance(fromDict, list)):
            if len(fromDict) > 0:
                fromDict = fromDict[0]
            else:
                raise Exception('Grupo constructor fromDict invalid')

        super().__init__(fromDict)
