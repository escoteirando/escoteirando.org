from escoteirando.ext.auth import AuthStatus, UserAuth
from escoteirando.ext.database import db


def test_login():
    ua = UserAuth(db)
    assert ua.verify_user('guionardo', '1234') == AuthStatus.OK


def test_signup():
    pass


def test_logout():
    pass


def test_lost_pass():
    pass
