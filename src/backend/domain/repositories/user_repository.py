from infra import BaseConnection
from infra.decorators import singleton
from domain.models.user import User


@singleton
class UserRepository(BaseConnection):

    def get(self, user_name) -> User:
        dbu = User.objects(user_name=user_name)[0:1]
        dbu = None if len(dbu) == 0 else dbu[0]
        print(f'User.get({user_name}) = {str(dbu)}')
        return dbu

    def update(self, user: User) -> bool:
        if user is None:
            return False

    def delete(self, user: User) -> bool:
        if user is None:
            return False
