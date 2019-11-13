from .basemodel import BaseModel


class Escotista(BaseModel):

    def __init__(self, content):
        super().__init__(content)
        [self.ativo, self.codigo, self.codigoAssociado, self.codigoFoto, self.codigoGrupo, self.codigoRegiao, self.nomeCompleto, self.username] = self.get(
            ['ativo', 'codigo', 'codigoAssociado', 'codigoFoto', 'codigoGrupo', 'codigoRegiao',        'nomeCompleto', 'username'])
