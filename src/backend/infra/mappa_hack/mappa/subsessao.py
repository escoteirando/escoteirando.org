from .basemodel import BaseModel
from .associado import Associado


class Subsessao(BaseModel):

    def __init__(self, content):
        super().__init__(content)
        [self.codigo, self.nome, self.codigoSecao, self.codigoLider, self.codigoViceLider, associados] = self.get(['codigo', 'nome',
                                                                                                                   'codigoSecao', 'codigoLider', 'codigoViceLider', 'associados'])

        self.associados = []
        for associado in associados:
            cassociado = Associado(associado)
            if cassociado.ok:
                self.associados.append(cassociado)
            else:
                self.content = "ERROR"
                return
