from infra import BaseConnection
from infra.decorators import singleton
from domain.models.user import User


@singleton
class UsersRepository(BaseConnection):

    def __init__(self):
        self.collection = self.db.get_collection('users')

    def get(self, userid) -> User:
        dbu = self.collection.find_one({"id": userid})

        if dbu is None:
            return None

        return User(dbu)

    def put(self, user: User)->bool:
        dbu = user.__dict__
        result = self.collection.insert_one(dbu)
        return result.inserted_id is not None


