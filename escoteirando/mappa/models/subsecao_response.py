from .basemodel import BaseModel
from .associado_response import Associado


class Subsecao(BaseModel):

    def __init__(self, content):
        self.codigo = None
        self.nome = None
        self.codigoSecao = None
        self.codigoLider = None
        self.codigoViceLider = None
        self.associados = None
        super().__init__(content)

        associados = []

        for associado in self.associados:
            cassociado = Associado(associado)
            associados.append(cassociado)

        self.associados = associados
