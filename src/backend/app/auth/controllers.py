""" app.auth.controllers """

from flask import Blueprint
from flask_api import status

from app.tools import request_values, response
from domain.services.user_service import UserService

auth = Blueprint('auth', __name__)


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

    if not username:
        return response("username required",
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if not password:
        return response("password required",
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    user = UserService().get_user(username)

    user_error = user is None
    if not user_error:
        user_error = not UserService().check_password(user, password)

    if user_error:
        return response("username or password error",
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    UserService().set_logged_user(user)
    return response("user logged in")


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
        return response("username required",
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if not password:
        return response("password required",
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
