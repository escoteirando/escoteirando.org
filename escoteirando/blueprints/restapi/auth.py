from flask import Blueprint, request, make_response
from escoteirando.ext.auth import verify_login

auth = Blueprint('auth', __name__, url_prefix='/api/v1')
logger = getLogger()


@auth.route('/login', methods=['POST'])
def login():
    if not ('username' in request.form and 'password' in request.form):
        return {"msg": "Invalid request arguments"}, 400
    username = request.form['username']
    password = request.form['password']
    remember_me = False if 'remember' not in request.form else (
        request.form['remember'].upper() == 'TRUE')
    user_auth = UserAuth()
    existing_user = user_auth.get_user(username)
    auth_status = user_auth.verify_user(existing_user, password)
    if auth_status is AuthStatus.NOT_FOUND:
        return {"msg": "User not found"}, 403
    if auth_status is AuthStatus.PASSWORD_ERROR:
        return {"msg": "Password error"}, 403
    user_auth.do_login(existing_user)
    return {"msg": f"Username:{username} | Password:{password}"}, 200


@auth.route('/user', methods=['GET'])
def user():
    lu = UserAuth().logged_user()
    if not lu.is_authenticated:
        return {"msg": "User is not authenticated"}, 203

    return {"msg": lu}, 200


@auth.route('/logout', methods=['GET'])
def logout():
    UserAuth().do_logout()
    return 'logout', 200


@auth.route('/signup')
def signup():
    return 'signup'


@auth.route('/lostpass')
def lostpass():
    return "lostpass"
