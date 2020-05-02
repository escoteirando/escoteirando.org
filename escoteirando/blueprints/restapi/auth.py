import datetime
from flask import Blueprint, request

from escoteirando.domain.models.user import User
from escoteirando.ext.auth import AuthStatus, UserAuth, create_user
from escoteirando.ext.logging import get_logger

auth = Blueprint('auth', __name__, url_prefix='/api/v1')
logger = get_logger()


@auth.route('/test', methods=['GET', 'POST'])
def test():
    return {
        "msg": "TESTING",
        "when": datetime.datetime.now()
    }


@auth.route('/login', methods=['POST'])
def login():
    if not ('username' in request.form and 'password' in request.form):
        logger.error('LOGIN = %s', 'INVALID REQUEST')
        return {"msg": "Invalid request arguments"}, 400
    username = request.form['username']
    password = request.form['password']
    remember_me = False if 'remember' not in request.form else (
        request.form['remember'].upper() == 'TRUE')
    user_auth = UserAuth()
    existing_user = user_auth.load_user(username)
    auth_status = user_auth.verify_user(existing_user, password)
    logger.info('LOGIN(%s,%s,%s) = %s',
                username,
                password,
                remember_me,
                auth_status)
    if auth_status is AuthStatus.NOT_FOUND:
        return {"msg": "User not found"}, 403
    if auth_status is AuthStatus.PASSWORD_ERROR:
        return {"msg": "Password error"}, 403
    user_auth.do_login(existing_user, remember_me)
    return {"msg": f"Username:{username} | Password:{password}"}, 200


@auth.route('/user', methods=['GET'])
def user():
    lu: User = UserAuth().logged_user()
    if not lu.is_authenticated:
        return {"msg": "User is not authenticated"}, 203

    return {
        "msg":
            {
                "id": lu.id,
                "username": lu.username,
                "email": lu.email
            }
    }, 200


@auth.route('/logout', methods=['GET'])
def logout():
    lu: User = UserAuth().logged_user()
    if not lu.is_authenticated:
        user_msg = "User is not authenticated"
    else:
        user_msg = {
            "id": lu.id,
            "username": lu.username,
            "email": lu.email
        }
    logger.info('LOGOUT %s', user_msg)
    res = {"msg": user_msg}
    UserAuth().do_logout()
    return res, 200


@auth.route('/signup', methods=['POST'])
def signup():
    if not ('username' in request.form and 'password' in request.form):
        logger.error('LOGIN = %s', 'INVALID REQUEST')
        return {"msg": "Invalid request arguments"}, 400
    username = request.form['username']
    password = request.form['password']

    try:
        create_user(username, password)
    except Exception as exc:
        return {"msg": str(exc)}, 400

    return {"msg": "OK"}


@auth.route('/lostpass')
def lostpass():
    return "lostpass"
