from .basemodel import BaseModel


class Escotista(BaseModel):
    """ Escotista response
    {
        "codigo": 50442, 
        "codigoAssociado": 850829, 
        "username": "Guionardo", 
        "nomeCompleto": "GuionardoFurlan",
        "ativo": "S", 
        "codigoGrupo": 32, 
        "codigoRegiao": "SC", 
        "codigoFoto": null
    }
    """

    def __init__(self, fromDict):
        self.ativo = None
        self.codigo = None
        self.codigoAssociado = None
        self.codigoFoto = None
        self.codigoGrupo = None
        self.codigoRegiao = None
        self.nomeCompleto = None
        self.username = None
        super().__init__(fromDict)
