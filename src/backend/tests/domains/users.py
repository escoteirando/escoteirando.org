from domain.repositories import UsersRepository
from domain.models import User

ur = UsersRepository()


def Test01():
    user = ur.get("1")
    print(user)