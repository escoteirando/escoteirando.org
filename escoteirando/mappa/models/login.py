from .basemodel import BaseModel


class Login(BaseModel):
    """
    Login Model
    {
        "id": "904QVxCGR0mLG6uDqWt7EOZLZZyfbaBRatKnoMefohwfkpPjc5jeuyUNAWED5t7H",
        "ttl": 1209600,
        "created": "2019-10-26T02:19:09.146Z",
        "userId": 50442
    }
    """

    def __init__(self, fromDict=None):
        self.id = None
        self.ttl = None
        self.created = None
        self.userId = None

        super().__init__(fromDict)

        {
            "id": "904QVxCGR0mLG6uDqWt7EOZLZZyfbaBRatKnoMefohwfkpPjc5jeuyUNAWED5t7H",
            "ttl": 1209600,
            "created": "2019-10-26T02:19:09.146Z",
            "userId": 50442
        }
