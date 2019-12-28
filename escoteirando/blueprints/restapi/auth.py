from flask import Blueprint, request, make_response


auth = Blueprint('auth', __name__, url_prefix='/api/v1')


@auth.route('/login')
def login():
    if request.method != 'POST':
        return {'message': 'INVALID METHOD FOR LOGIN'}, 405
    
    return 'login'


@auth.route('/signup')
def signup():
    return 'signup'


@auth.route('/logout')
def logout():
    return 'logout'


@auth.route('/lostpass')
def lostpass():
    return "lostpass"
