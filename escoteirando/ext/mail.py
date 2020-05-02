import flask_mail
from flask import Flask

mail = flask_mail.Mail()


def init_app(app: Flask):
    mail.init_app(app)
