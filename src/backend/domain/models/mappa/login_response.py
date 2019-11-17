from datetime import datetime, timedelta
from ..basemodel import BaseModel


class Authentication(BaseModel):
    """ Login Authentication Info

    {
        "id":"904QVxCGR0mLG6uDqWt7EOZLZZyfbaBRatKnoMefohwfkpPjc5jeuyUNAWED5t7H",
        "ttl":1209600,
        "created": "2019-10-26T02:19:09.146Z",
        "userId":50442
    }
    """

    def __init__(self, fromDict):
        self.id = None
        self.ttl = None
        self.created = ''
        self.userId = None

        super().__init__(fromDict)

        self.valid = datetime.strptime(
            self.created[0:19], '%Y-%m-%dT%H:%M:%S')+timedelta(seconds=self.ttl)
