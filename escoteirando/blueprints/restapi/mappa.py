from time import time

from flask import Blueprint
from flask import current_app as app
from flask import request
from flask_login import current_user

from escoteirando.domain.models.user import User, db
from escoteirando.domain.services.infra.service_user import ServiceUser
from escoteirando.ext.logging import getLogger
from mappa.service.mappa_service import MAPPAService

mappa_bp = Blueprint('mappa', __name__, url_prefix='/api/v1/mappa')
logger = getLogger()


@mappa_bp.route('/login', methods=['POST'])
def login():
    """ Tries to login on MAPPA """
    if not ('username' in request.form and 'password' in request.form):
        return {"msg": "Invalid request arguments"}, 400
    username = request.form['username']
    password = request.form['password']
    mappa: MAPPAService = app.mappa

    if not mappa.login(username, password):
        return {"msg": "Invalid login"}, 401

    user_info = mappa.get_user_info(mappa.user_id)

    su = ServiceUser(db)
    if su.save_user(user_info):
        logger.info('MAPPA login OK: %s', username)
        return {
            "msg": "MAPPA login OK",
            "user_info": user_info.to_dict()}, 200
    logger.warning('MAPPA login OK: %s - ERROR ON SAVING', username)
    return {"msg": "ERROR ON SAVING USER DATA"}, 400


@mappa_bp.route('/secao', methods=['GET'])
def get_secao():
    mappa: MAPPAService = app.mappa
    if not validate_mappa_user_auth():
        return {'msg': 'UNAUTHORIZED MAPPA API'}, 401
    
    secoes = mappa.get_secoes(mappa.user_id)
    if secoes:
        return {
            "msg": "OK",
            "secoes": [secao.to_dict() for secao in secoes]}, 200

    return {"msg": "No sections"}, 400


def validate_mappa_user_auth():
    mappa: MAPPAService = app.mappa
    user: User = current_user
    if mappa.is_authorized(user.user_id):
        return True

    if user.auth_valid_until > time():
        mappa.set_authorization(
            user.user_id, user.authorization, user.auth_valid_until)
        return True

    return False
