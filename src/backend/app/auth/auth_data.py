import base64
from json import dumps, loads

from flask import session

from domain.models.user import User

SESSION_USER_DATA = base64.b64encode(
    "userdata".encode('utf-8')).decode('utf-8')


class LoggedUser:
    _user = None

    @classmethod
    def getUser(cls) -> User:
        print(f"getUser [{SESSION_USER_DATA}]")
        print(str(cls._user))
        print(session)
        if cls._user is None and SESSION_USER_DATA in session:
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
