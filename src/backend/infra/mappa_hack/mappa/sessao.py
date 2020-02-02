from .basemodel import BaseModel


class Sessao(BaseModel):

    def __init__(self, content):
        super().__init__(content)
        [self.codigo, self.nome, self.codigoTipoSecao, self.codigoGrupo, self.codigoRegiao] = self.get(
            ['codigo', 'nome', 'codigoTipoSecao', 'codigoGrupo', 'codigoRegiao'])

        #[{"codigo":1424,"nome":"ALCATÉIA 1 ","codigoTipoSecao":1,"codigoGrupo":32,"codigoRegiao":"SC"}]
