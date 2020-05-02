from time import time

from flask_login import current_user
from orjson import dumps, loads

from escoteirando.domain.models.user import User
from mappa.models.internal.user_info import UserInfoModel
from mappa.models.mappa.secao import SecaoModel
from mappa.service.mappa_service import MAPPAService
from ..base_service import BaseService


class ServiceUser(BaseService):

    LOG_INFO = 'ServiceUser'

    def __init__(self, db):
        super().__init__(db)
        self.mappa = MAPPAService(self.configs.CACHE_STRING_CONNECTION)

    def save_user(self, user_info: UserInfoModel):
        user: User = current_user
        upd_user: User = user.query.get(user.id)
        upd_user.user_id = user_info.id
        upd_user.user_name = user_info.user_name
        upd_user.authorization = user_info.autorizacao
        upd_user.auth_valid_until = user_info.autorizacao_validade
        upd_user.codigo_associado = user_info.cod_associado
        upd_user.codigo_regiao = user_info.cod_regiao
        upd_user.codigo_grupo = user_info.cod_grupo
        upd_user.nome_grupo = user_info.nom_grupo
        upd_user.nome = user_info.nome_completo
        upd_user.data_nascimento = user_info.data_nascimento
        upd_user.sexo = user_info.sexo

        try:
            self.DB.session.commit()
            self.log.info('%s: USER SAVED %s',
                          self.LOG_INFO, upd_user.user_name)
            cache_data = dumps(upd_user.to_dict()).decode()
            self.cache.set_value('user', str(
                user.id), cache_data, user_info.autorizacao_validade - time())
            return True
        except Exception as exc:
            self.log.exception('%s: ERROR ON SAVING %s - %s',
                               self.LOG_INFO, upd_user.user_name, exc)

        return False

    def current_user(self) -> UserInfoModel:
        """ Obter o UserInfo do usuário logado """
        if not current_user:
            return None

        cache_data = loads(self.cache.get_value('user', str(current_user.id)))
        if cache_data:
            user = UserInfoModel(cache_data)
            self.mappa.set_authorization(
                user.user_id, user.autorizacao, user.autorizacao_validade)
            return user

        upd_user: User = current_user.query.get(current_user.id)
        if upd_user:
            # TODO: Atualizar cache do current_user
            user = {
                "id": current_user.id,
                "user_name": upd_user.user_name,
                "autorizacao": '',
                "autorizacao_validade": 0,
                "cod_associado": upd_user.codigo_associado,
                "cod_regiao": upd_user.codigo_regiao,
                "cod_grupo": upd_user.codigo_grupo,
                "nom_grupo": upd_user.nome_grupo,
                "nome_completo": upd_user.nome,
                "data_nascimento": upd_user.data_nascimento,
                "sexo": upd_user.sexo
            }
            infomodel = UserInfoModel(user)

            cache_data = dumps(upd_user.to_dict())
            self.cache.set_value('user', str(
                upd_user.id), cache_data,
                infomodel.autorizacao_validade - time())
            return infomodel

        return None

    def get_secoes(self):
        # TODO: Retornar seções do usuário
        secoes = self.mappa.get_secoes(self.mappa._user_id)
        return secoes
