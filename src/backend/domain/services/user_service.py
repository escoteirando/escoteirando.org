import base64
from json import dumps, loads

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from infra.config import config
from infra.decorators import singleton
from infra.log import logging

SESSION_USER_DATA = base64.b64encode(
    "userdata".encode('utf-8')).decode('utf-8')

logger = logging.getLogger(__name__)


@singleton
class UserService:

    def __init__(self):
        self.repository = UserRepository()
        self.logged_user: User = None

    def set_logged_user(self, user: User) -> bool:
        if isinstance(user, User):
            self.logged_user = user
            session.clear()
            dic = user.as_dict
            session[SESSION_USER_DATA] = dumps(dic)
            return True

        return False

    def get_logged_user(self) -> User:
        if self.logged_user is None and SESSION_USER_DATA in session:
            user = loads(session[SESSION_USER_DATA])
            try:
                logged_user = User()
                logged_user.as_dict = user
                self.logged_user = logged_user
            except Exception as e:
                logger.exception(e)

        return self.logged_user

    def login(username: str, password: str):
        user = UserRepository().get(username)
        if check_password_hash(user.password, password):
            return
