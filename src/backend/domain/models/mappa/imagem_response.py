from ..basemodel import BaseModel

class ImagemResponse(BaseModel):
    '''
    Imagem

    REQUEST GET /api/imagens/{id}

    {
        "imagem": "base64 image",
        "id": 9190
    }    
    '''
    def __init__(self, fromDict):
        self.imagem = None
        self.id = None
        super().__init__(fromDict)

