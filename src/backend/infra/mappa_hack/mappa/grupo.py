from .basemodel import BaseModel


class Grupo(BaseModel):

    def __init__(self, content):
        super().__init__(content)
        [self.codigo, self.codigoRegiao, self.nome, self.codigoModalidade] = self.get(
            ['codigo', 'codigoRegiao', 'nome', 'codigoModalidade'])

    #[{"codigo":32,"codigoRegiao":"SC","nome":"LEÕES DE BLUMENAU","codigoModalidade":1}]
