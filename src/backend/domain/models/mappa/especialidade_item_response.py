from ..basemodel import BaseModel


class EspecialidadeItem(BaseModel):
    """ Especialidade Item Response
    {
        "id": 1,
        "codigoEspecialidade": 1,
        "descricao": "Montar, desmontar, dobrar e acondicionar uma barraca.",
        "numero": 1
    }
    """

    def __init__(self, fromDict):
        self.id = None
        self.codigoEspecialidade = None
        self.descricao = None
        self.numero = None
        super().__init__(fromDict)
