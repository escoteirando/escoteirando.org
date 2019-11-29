from flask import Blueprint
from flask_api import status

from ..auth import SESSION_USER_DATA, LoggedUser
from ..tools import response, request_values
from domain.services.mappa import login
from domain.services.mappa.request import authIsValid, post, setAuth, _userId, getAuth
from domain.services.mappa.escotista import escotista
from domain.services.mappa.associado import associado
from domain.repositories.users_repository import UsersRepository

# TODO: REMOVE REPOSITORY FROM CONTROLLER

mappa = Blueprint('mappa', __name__)


@mappa.route('/')
def index():
    return "mAPPa"


@mappa.route('/fetch_user')
def fetch_user():
    if not LoggedUser.getUser():
        return response({"message": "user is not logged"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    mappa_password = request_value('mappa_password')
    if not mappa_password:
        return response("mappa_password required", status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    user = LoggedUser.getUser()

    if not login(user.user_name_mappa, mappa_password):
        return response("login error in mappa", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    auth = getAuth()
    if not auth['userid']:
        return response("login error in mappa - no userid", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    esc = escotista(auth['userid'])

    if not esc:
        return response("error getting escotista")
    print(esc)
    ass = associado(esc.codigoAssociado)
    if not ass:
        return response("error getting associado")
    print(ass)

    user.full_name = ass.nome
    user.codigo_associado = ass.codigo
    UsersRepository().post(user)

    return response({'message': 'OK', 'user': user.toDict()}, status.HTTP_200_OK)


@mappa.before_request
def _load_logged_in_user():
    LoggedUser.getUser()
