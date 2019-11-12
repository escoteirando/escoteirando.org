from . import BaseModel

class User(BaseModel):

    def __init__(self, fromDict=None):
        self.id = None
        self.user_name = None
        super().__init__(fromDict)
        