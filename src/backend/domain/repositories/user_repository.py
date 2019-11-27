from infra import BaseConnection
from domain.models.user import User
from domain.models.ue.associado import Associado
from .ue_repository import UERepository


class UserRepository(BaseConnection):
    ue_repo = UERepository()

    def get(self, user_name) -> User:
        dbu = User.objects(user_name=user_name)
        dbu = None if len(dbu) == 0 else dbu[0]
        print(f'User.get({user_name}) = {str(dbu)}')
        return dbu

    def update(self, user: User) -> bool:
        if user is None:
            return False

    def delete(self, user: User) -> bool:
        if user is None:
            return False

    def post(self, user: User) -> bool:
        if user is None:
            return False
        if isinstance(user.associado, Associado) or\
                user.associado.document_type == Associado:
            if user.associado.id is None:
                self.ue_repo.post_associado(user.associado)

        return user.save()
