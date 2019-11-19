from . import BaseModel


class User(BaseModel):

    def __init__(self, fromDict=None):
        self.user_name = None
        self.user_name_mappa = None
        self.password = None
        self.full_name = None
        self.codigo_associado = None
        super().__init__(fromDict)
