import base64
from json import loads, dumps

from flask import session

from domain.models.user import User

SESSION_USER_DATA = str(base64.b64encode("userdata".encode('utf-8')))


class LoggedUser:
    _user = None

    @classmethod
    def getUser(cls) -> User:
        if cls._user is None and session[SESSION_USER_DATA]:
            cls._user = User(loads(session[SESSION_USER_DATA]))

        return cls._user

    @classmethod
    def setUser(cls, user: User):
        if isinstance(user, User):
            cls._user = user
            session.clear()
            dic = user.toDict()
            session[SESSION_USER_DATA] = dumps(dic)

    @classmethod
    def logoutUser(cls):
        cls._user = None
        session.clear()
