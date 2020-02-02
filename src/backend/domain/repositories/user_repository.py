from domain.models.ue.associado import Associado
from domain.models.user import User
from infra.data.baseconnection import BaseConnection

from .ue_repository import UERepository


class UserRepository(BaseConnection):
    ue_repo = UERepository()

    def get(self, user_name) -> User:
        dbu = User.objects(user_name=user_name)
        dbu = None if len(dbu) == 0 else dbu[0]
        self.logger.info('User.get(%s) = %s', user_name, dbu)
        return dbu

    def delete(self, user: User) -> bool:
        if user is None:
            return False
        if user.associado is not None and \
                (isinstance(user.associado, Associado) or
                 user.associado.document_type == Associado):
            self.ue_repo.delete_associado(user.associado)
        try:
            user.delete()
            return True
        except Exception as del_exception:
            self.logger.exception("EXCEPTION DELETING USER: %s", del_exception)
        return False

    def post(self, user: User) -> bool:
        if user is None:
            return False
        if user.associado is not None and \
                (isinstance(user.associado, Associado) or
                 user.associado.document_type == Associado):
            if user.associado.id is None:
                self.ue_repo.post_associado(user.associado)
        try:
            user = user.save()
            return True
        except Exception as post_exception:
            self.logger.exception("EXCEPTION POSTING USER: %s", post_exception)
            return False
