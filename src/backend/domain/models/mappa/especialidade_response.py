from ..basemodel import BaseModel
from .especialidade_item_response import EspecialidadeItem


class Especialidade(BaseModel):
    """ Especialidade Response
     {
        "codigo": 1,
        "descricao": "Acampamento",
        "ramoConhecimento": "HABILIDADES_ESCOTEIRAS",
        "prerequisito": "Ter acampado com a seção ou patrulha por um mínimo: 6 noites para o Nível 1; 12 noites para o Nível 2; e 18 noites para o Nível 3.",
        "itens": [
            {
                "id": 1,
                "codigoEspecialidade": 1,
                "descricao": "Montar, desmontar, dobrar e acondicionar uma barraca.",
                "numero": 1
            },...
        ]
    }
    """

    def __init__(self, fromDict):
        self.codigo = None
        self.descricao = None
        self.ramoConhecimento = None
        self.prerequisito = None
        self.itens = []
        super().__init__(fromDict)

        for item in self.itens:
            item = EspecialidadeItem(item)
