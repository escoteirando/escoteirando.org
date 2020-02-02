from .basemodel import BaseModel
from .item import Item

class Especialidade(BaseModel):

    def __init__(self, content):
        super().__init__(content)
        [self.codigo, self.descricao, self.ramoConhecimento, self.prerequisito, itens] = self.get(
            ['codigo', 'descricao', 'ramoConhecimento', 'requisito', 'itens'])
        self.itens = []
        if (content is None):
            for item in itens:
                citem = Item(item)
                if citem.ok:
                    self.itens.append(citem)
