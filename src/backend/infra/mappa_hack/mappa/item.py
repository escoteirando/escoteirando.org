from .basemodel import BaseModel


class Item(BaseModel):

    def __init__(self, content):
        super().__init__(content)
        [self.id, self.codigoEspecialidade, self.descricao, self.numero] = self.get(
            ['id', 'codigoEspecialidade', 'descricao', 'numero'])
