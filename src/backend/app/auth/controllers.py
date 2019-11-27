""" app.auth.controllers """

from flask import Blueprint, Response, request, session
from flask_api import status
from werkzeug.security import check_password_hash, generate_password_hash

from app.tools import request_values, response
from domain.models.user import User
from domain.repositories import UsersRepository

from . import SESSION_USER_DATA, LoggedUser

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    return response("AUTH")


@auth.route('/logout', methods=['GET'])
def logout():
    LoggedUser.logoutUser()
    return response('User logout')


@auth.route('/login', methods=['POST'])
def login():
    [username, password] = request_values('username', 'password')

    if not username:
        return response("username required", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if not password:
        return response("password required", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    user_repository = UsersRepository()
    user = user_repository.get(username)

    user_error = user is None
    if not user_error:
        user_error = not check_password_hash(user.password, password)

    if user_error:
        return response("username or password error", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    LoggedUser.setUser(user)
    return response("user logged in")


@auth.before_request
def _load_logged_in_user():
    LoggedUser.getUser()


@auth.route('/current_user')
def current_user():
    if not LoggedUser.getUser():
        return response({"user": None}, status=status.HTTP_200_OK)

    return response({"user": LoggedUser.getUser().toDict()}, status=status.HTTP_200_OK)


@auth.route('/register', methods=['POST'])
def register_normal():
    [username, password, username_mappa] = request_values(
        'username', 'password', 'username_mappa')
    if not username:
        return response({"message": "username required"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if not password:
        return response({"message": "password required"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if not username_mappa:
        return response({'message': 'username_mappa required'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    user_repository = UsersRepository()
    user = user_repository.get(username) or user_repository.get(
        username_mappa, 'user_name_mappa')
    if user:
        return response({"message": "user preexistent"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    user = User({'user_name': username,
                 'user_name_mappa': username_mappa,
                 'password': generate_password_hash(password)})
    if user_repository.put(user):
        return response({'message': 'user created'}, status=status.HTTP_201_CREATED)

    return response({'message': 'error on create user'}, status=status.HTTP_409_CONFLICT)
