from infra import BaseConnection
from domain.models.ue.associado import Associado


class UERepository(BaseConnection):

    def get_associado(self, key) -> Associado:
        if isinstance(key, int):
            dba = Associado.objects(codigo=key)
        elif isinstance(key, str):
            dba = Associado.objects(id=key)
        else:
            return None

        dba = None if len(dba) == 0 else dba[0]
        return dba

    def post_associado(self, associado: Associado) -> bool:
        if associado is None:
            return False
        try:
            associado.save()
            return True
        except Exception as post_exception:
            self.logger.exception('POST ASSOCIADO: %s', post_exception)

            return False

    def delete_associado(self, associado: Associado) -> bool:
        if associado is None:
            return False
        try:
            associado.delete()
            return True
        except Exception as e:
            return False
