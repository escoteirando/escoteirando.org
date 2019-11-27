from domain.repositories.user_repository import UserRepository

ur = UserRepository()
assert isinstance(ur, UserRepository)
