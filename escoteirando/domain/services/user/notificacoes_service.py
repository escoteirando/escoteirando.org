from datetime import datetime

from escoteirando.domain.models.notificacao import Notificacao

from ..base_service import BaseService


class NotificacoesService(BaseService):

    LOG_INFO = 'NotificacoesService'
    # TODO: Implementar service de notificações

    def get_notificacoes_usuario(self, user_id: int):
        pass

    def add_notificacao(self, user_id: int, mensagem: str, link: str, valida_ate: datetime):
        pass
