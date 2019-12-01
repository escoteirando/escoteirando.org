from flask import Blueprint
from flask_api import status

from domain.services.mappa import MappaLoginService
from domain.services.user_service import UserService
from infra.config import config

from ..tools import request_values, response

mappa = Blueprint('mappa', __name__)
user_service = UserService()

if config.MAPPA_ENABLED:
    mappa_service = MappaLoginService()


@mappa.route('/')
def index():
    return "mAPPa"


@mappa.route('/fetch_user')
def fetch_user():
    """ Obter informações do escotista e associado a partir do mAPPa
    Usuário deve estar logado no sistema
    """
    user = user_service.get_logged_user()
    if not user:
        return response(
            {"message": "user is not logged"},
            status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    mappa_password = request_values('mappa_password')
    if not mappa_password:
        return response("mappa_password required",
                        status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    if not mappa_service.login(user.user_name_mappa, mappa_password):
        return response("login error in mappa",
                        status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if not mappa_service.auth_data.id:
        return response("login error in mappa - no userid",
                        status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    esc = mappa_service.get_escotista(mappa_service.auth_data.id)

    if not esc:
        return response("error getting escotista")
    # TODO: Remove print
    print(esc)
    ass = mappa_service.get_associado(esc.codigoAssociado)
    if not ass:
        return response("error getting associado")
    print(ass)

    user.full_name = ass.nome
    user.codigo_associado = ass.codigo

    user_service.update_user(user)

    return response({'message': 'OK', 'user': user.toDict()},
                    status.HTTP_200_OK)


@mappa.before_request
def _load_logged_in_user():
    user_service.get_logged_user()
