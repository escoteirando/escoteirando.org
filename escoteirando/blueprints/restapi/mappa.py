from time import time

from flask import Blueprint
from flask import current_app as app
from flask import make_response, request
from flask_login import current_user

from escoteirando.domain.enums import CodigoModalidade, TipoSecao
from escoteirando.domain.models.mappa.grupo import MAPPA_Grupo
from escoteirando.domain.models.mappa.progressao import MAPPA_Progressao
from escoteirando.domain.models.user import User, db
from escoteirando.domain.services.infra.service_infra import ServiceInfra
from escoteirando.domain.services.mappa.service_grupo import ServiceGrupo
from escoteirando.domain.services.mappa.service_secao import ServiceSecao
from escoteirando.ext.logging import getLogger
from escoteirando.mappa.mappa import Mappa

mappa_bp = Blueprint('mappa', __name__, url_prefix='/api/v1/mappa')
logger = getLogger()


@mappa_bp.route('/login', methods=['POST'])
def login():
    if not ('username' in request.form and 'password' in request.form):
        return {"msg": "Invalid request arguments"}, 400
    username = request.form['username']
    password = request.form['password']
    mappa: Mappa = app.mappa

    if not mappa.login(username, password):
        return {"msg": "Invalid login"}, 400

    infra = ServiceInfra(db)
    last_fetch_progressoes = float(infra.get_param(
        'MAPPA_LAST_FETCH_PROGRESSOES', 0, "0"))

    if time()-last_fetch_progressoes > 604800:  # Mais de uma semana
        progressoes = mappa.get_progressoes()
        sec = db.create_scoped_session()
        for progressao in progressoes:
            mp = MAPPA_Progressao.query.filter(
                MAPPA_Progressao.codigo == progressao.codigo).first()
            if not mp:
                mp = MAPPA_Progressao()

            mp.codigo = progressao.codigo
            mp.descricao = progressao.descricao
            mp.codigoUeb = progressao.codigoUeb
            mp.codigoCaminho = progressao.codigoCaminho
            mp.codigoCompetencia = progressao.codigoCompetencia
            mp.codigoDesenvolvimento = progressao.codigoDesenvolvimento
            mp.segmento = progressao.segmento
            mp.ordenacao = progressao.ordenacao
            if mp.codigoCaminho in [1, 2, 3]:
                mp.ramo = TipoSecao.ALCATEIA
            elif mp.codigoCaminho in [4, 5, 6]:
                mp.ramo = TipoSecao.TROPA_ESCOTEIRA
            elif mp.codigoCaminho in [11, 12]:
                mp.ramo = TipoSecao.TROPA_SENIOR
            elif mp.codigoCaminho in [15, 16]:
                mp.ramo = TipoSecao.CLA_PIONEIRO

            if not mp.id:
                sec.add(mp)

        try:
            sec.commit()
            infra.set_param('MAPPA_LAST_FETCH_PROGRESSOES', str(time()), 0)
            logger.info('Update progressoes: %s', len(progressoes))
        except Exception as exc:
            logger.exception('Exception on update progressoes: %s', exc)

    user: User = current_user

    update_grupo = False
    update_secao = False

    upd_user: User = user.query.get(user.id)
    upd_user.user_id = mappa.userId
    upd_user.user_name = mappa.userName
    upd_user.authorization = mappa.authorization
    upd_user.auth_valid_until = mappa.auth_valid_until
    upd_user.codigo_associado = mappa.codigoAssociado
    if mappa.get_grupo(mappa.codigoGrupo, mappa.codigoRegiao):
        update_grupo = upd_user.codigo_grupo != mappa.codigoGrupo
        upd_user.codigo_grupo = mappa.codigoGrupo
    if mappa.get_secao(mappa.userId):
        update_secao = upd_user.codigo_secao != mappa.codigoSecao
        upd_user.codigo_secao = mappa.codigoSecao
    upd_user.codigo_regiao = mappa.codigoRegiao
    upd_user.nome = mappa.nomeAssociado
    upd_user.sexo = 'M' \
        if mappa.sexo.upper().startswith('M') else \
        'F' if mappa.sexo.upper().startswith('F') else \
        'O'
    upd_user.data_nascimento = mappa.dataNascimento

    if update_grupo:
        service_grupo = ServiceGrupo(db)
        ex_grupo = mappa.get_grupo(mappa.codigoGrupo, mappa.codigoRegiao)
        service_grupo.set_grupo(ex_grupo)

    if update_secao:
        service_secao = ServiceSecao(db)
        ex_secao = mappa.get_secao(mappa.userId)
        service_secao.set_secao(ex_secao)

    try:
        db.session.commit()
        logger.info('MAPPA login OK: %s', username)
        return {"msg": "MAPPA login OK"}, 200
    except Exception as exc:
        logger.exception('MAPPA login exception: %s', exc)
        return {"msg": str(exc)}, 400
