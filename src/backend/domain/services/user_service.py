import base64
from json import dumps, loads

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from domain.models.user import User
from domain.repositories.user_repository import UserRepository

from infra.log import logging

SESSION_USER_DATA = base64.b64encode(
    "userdata".encode('utf-8')).decode('utf-8')

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self):
        self.repository = UserRepository()
        self.logged_user: User = None

    def set_logged_user(self, user: User) -> bool:
        if isinstance(user, User):
            self.logged_user = user
            if session:
                session.clear()
                dic = dict(user)
                session[SESSION_USER_DATA] = dumps(dic)
            return True

        return False

    def get_logged_user(self) -> User:
        '''
        Returns logged user or None
        '''
        if self.logged_user is None and SESSION_USER_DATA in session:
            user = loads(session[SESSION_USER_DATA])
            try:
                logged_user = User()
                logged_user.as_dict = user
                self.logged_user = logged_user
            except Exception as e:
                logger.exception(e)

        return self.logged_user

    def login(self, username: str, password: str) -> bool:
        user = self.repository.get(username)
        if check_password_hash(user.password, password):
            self.set_logged_user(user)
            return True
        return False

    def logout(self):
        self.logged_user = None
        session.clear()

    def get_user(self, username: str) -> User:
        '''
        Returns the User or None if not found
        '''
        return self.repository.get(user_name=username)
    
    def create_user(self, username: str, password: str) -> (bool, str):
        if not username or len(username) < 6:
            return (False, 'USERNAME LENGHT INVALID')
        if not username.isalnum():
            return (False, 'USERNAME MUST CONTAINS ONLY LETTERS AND NUMBERS')
        if not password or len(password) < 6:
            return (False, 'PASSWORD LENGHT INVALID')
        if not (any([x.isdigit() for x in password]) and
                any([x.isupper() for x in password])):
            return (False, 'PASSWORD MUST CONTAINS LETTERS, NUMBERS, CAPITALS')

        user = self.get_user(username)
        if user:
            return (False, 'USER PREEXISTENT')
        user = User(user_name=username,
                    password=generate_password_hash(password),
                    level=0
                    )

        if self.repository.post(user):
            return (True, 'USER CREATED')

        return (False, 'USER NOT CREATED')
