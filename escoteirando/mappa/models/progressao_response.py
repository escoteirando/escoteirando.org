from .basemodel import BaseModel


class Progressao(BaseModel):
    """ Progressao Response
    {
        "codigo": 1,
        "descricao": "Ouvir o episódio \"Irmãos de Mowgli\" do Livro da Selva.",
        "codigoUeb": "S2",
        "ordenacao": 2,
        "codigoCaminho": 1,
        "codigoDesenvolvimento": 23,
        "numeroGrupo": null,
        "codigoRegiao": null,
        "codigoCompetencia": 38,
        "segmento": "PROMESSA_ESCOTEIRA_LOBINHO"
    }
    """

    def __init__(self, fromDict):
        self.codigo = None
        self.descricao = None
        self.codigoUeb = None
        self.ordenacao = None
        self.codigoCaminho = None
        self.codigoDesenvolvimento = None
        self.numeroGrupo = None
        self.codigoRegiao = None
        self.codigoCompetencia = None
        self.segmento = None
        super().__init__(fromDict)

    def __repr__(self):
        return "Progressao {0}:{1}".format(self.codigoUeb, self.descricao)
