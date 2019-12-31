""" app.auth.controllers """

from flask import Blueprint
from flask_api import status

from app.tools import request_values, response
from domain.services.user_service import userService as UserService
from infra.log import getLogger
from domain.services.mappa.mappa_login_service import MappaLoginService

auth = Blueprint('auth', __name__)
logger = getLogger('AUTH')

S_USERNAME_REQUIRED = 'Usuário não foi informado'
S_PASSWORD_REQUIRED = 'Senha não foi informada'
S_INVALID_CREDENTIALS = 'Usuário ou senha inválido(s)'
S_USER_LOGGED_IN = 'Usuário logado'


@auth.route('/')
def index():
    return response("AUTH")


@auth.route('/logout', methods=['GET'])
def logout():
    UserService().logout()
    return response('User logout')


@auth.route('/login', methods=['POST'])
def login():
    [username, password] = request_values('username', 'password')
    logger.info('LOGIN USERNAME: %s', username)
    if not username:
        return response(S_USERNAME_REQUIRED,
                        status=status.HTTP_401_UNAUTHORIZED)
    if not password:
        return response(S_PASSWORD_REQUIRED,
                        status=status.HTTP_401_UNAUTHORIZED)

    user = UserService().get_user(username)

    user_error = user is None
    if not user_error:
        user_error = not UserService().check_password(user, password)

    if user_error:
        mappa = MappaLoginService()
        if mappa.login(username, password):
            escotista = mappa.get_escotista(mappa.auth_data.userId)
            associado = mappa.get_associado(escotista.codigoAssociado)
            success, msg = UserService().create_user(username, password)
            if success:
                user = UserService().get_logged_user(username)
                user.associado = associado
                user.save()
                UserService().set_logged_user(user)
                return response(S_USER_LOGGED_IN)

        return response(S_INVALID_CREDENTIALS,
                        status=status.HTTP_401_UNAUTHORIZED)

    UserService().set_logged_user(user)
    return response(S_USER_LOGGED_IN)


@auth.before_request
def _load_logged_in_user():
    UserService().get_logged_user()


@auth.route('/current_user')
def current_user():
    cur_user = UserService().get_logged_user()
    if cur_user:
        cur_user = cur_user.user_name

    return response({"user": cur_user},
                    status=status.HTTP_200_OK)


@auth.route('/register', methods=['POST'])
def register_normal():
    [username, password, username_mappa] = request_values(
        'username', 'password', 'username_mappa')
    if not username:
        return response(S_USERNAME_REQUIRED,
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if not password:
        return response(S_PASSWORD_REQUIRED,
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if not username_mappa:
        return response('username_mappa required',
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    user = UserService().get_user(username)

    if user:
        return response("user preexistent",
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    success, message = UserService().create_user(username, password)

    if success:
        return response(message, status.HTTP_201_CREATED)

    return response(message, status.HTTP_409_CONFLICT)
