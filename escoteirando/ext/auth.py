from flask_simplelogin import SimpleLogin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from escoteirando.ext.database import db
from escoteirando.models.user import User

from enum import Enum


class AuthStatus(Enum):
    NOT_FOUND = 0
    PASSWORD_ERROR = 1
    NOT_VERIFIED = 2


class UserAuth:

    def __init__(self, db: SQLAlchemy):
        if not isinstance(db, SQLAlchemy):
            raise ValueError('db is not SQLAlchemy')
        self.db: SQLAlchemy = db

    def verify_user(self, username, password) -> AuthStatus:
        if not username or not password:
            return AuthStatus.NOT_FOUND
        existing_user:User = User.query.filter(
            User.username == username or User.email == username).first()

        if not existing_user:
            return AuthStatus.NOT_FOUND

        if not check_password_hash(existing_user.password, password):
            return AuthStatus.PASSWORD_ERROR

        if not existing_user.verified:
            return AuthStatus.NOT_VERIFIED
        existing_user.email
        if not existing_user.codigo_associado:
            return AuthStatus.NOT_MAPPA

        


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
    user = User(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user


def init_app(app):
    SimpleLogin(app, login_checker=verify_login)
