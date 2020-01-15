from flask_login import LoginManager
from werkzeug.security import check_password_hash, generate_password_hash

from escoteirando.ext.database import db as db
from escoteirando.models.user import User
from flask_login import LoginManager, login_user, logout_user, current_user

login_manager = LoginManager()

_login_manager = LoginManager()


class AuthStatus(Enum):
    NOT_FOUND = 0
    PASSWORD_ERROR = 1
    NOT_VERIFIED = 2
    NOT_MAPPA = 3
    OK = 9


class UserAuth:

    def __init__(self, _db: SQLAlchemy = None):
        if not _db:
            _db = db
        if not isinstance(_db, SQLAlchemy):
            raise ValueError('db is not SQLAlchemy')
        self.db: SQLAlchemy = _db

    def verify_user(self, username, password) -> AuthStatus:
        if not username or not password:
            return AuthStatus.NOT_FOUND
        existing_user: User = User.query.filter(
            User.username == username or User.email == username).first()

    def verify_user(self, user: User, password) -> AuthStatus:
        ''' Verify if a password authenticates a user '''
        if not user or not password:
            return AuthStatus.NOT_FOUND

        if not check_password_hash(user.password, password):
            return AuthStatus.PASSWORD_ERROR

        if not user.verified:
            return AuthStatus.NOT_VERIFIED
        
        if not existing_user.codigo_associado:
            return AuthStatus.NOT_MAPPA
        
        return AuthStatus.OK

    def do_logout(self):
        logout_user()



def verify_login(user):
    """Valida o usuario e senha para efetuar o login"""
    username = user.get('username')
    password = user.get('password')
    if not username or not password:
        return False
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        return False
    if check_password_hash(existing_user.password, password):
        return True
    return False


def create_user(username, password):
    """Registra um novo usuario caso nao esteja cadastrado"""
    if User.query.filter_by(username=username).first():
        raise RuntimeError(f'{username} ja esta cadastrado')
    user = User(id=0, username=username,
                password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user


@_login_manager.user_loader
def load_user(user_id):
    user = User.query.filter(
        User.email == user_id or User.user_id == user_id).first()

    return user


def init_app(app):
    _login_manager.init_app(app)

    # TODO: Remover SimpleLogin
    # SimpleLogin(app, login_checker=verify_login)
