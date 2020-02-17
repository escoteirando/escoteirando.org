import time

from flask import abort, render_template
from flask_login import current_user

from escoteirando.domain.models.mappa.secao import tipo_secao_str
from escoteirando.domain.models.user import User, db
from escoteirando.domain.services.mappa.service_grupo import ServiceGrupo
from escoteirando.domain.services.mappa.service_secao import ServiceSecao
from escoteirando.ext.jinja_tools import get_login_navbar, get_navbar
from escoteirando.ext.logging import get_logger
from escoteirando.models import Product

logger = get_logger()


def index():
    if current_user.is_anonymous:
        return _render_login()

    user: User = current_user
    if not user.codigo_associado or user.auth_valid_until < time.time():
        return _render_login_mappa()

    # TODO: Verificar o estado do usuario e apresentar a view correspondente
    return _render_index()


def view_test():
    return render_template("login_page.html",
                           navbar=get_login_navbar(),
                           page_title='Login')


def view_test_json():
    import datetime
    return {
        'testing': True,
        'when': datetime.datetime.now()
    }


def _render_index():
    panels = [
        {"title": "Estatísticas", "url": "#", "id": "stats"},
        {"title": "Últimas atividades", "url": "#", "id": "ult_atv"},
        {"title": "Estatísticas 2 ", "url": "#", "id": "stats"},
        {"title": "Últimas atividades 2", "url": "#", "id": "ult_atv"}
    ]
    service_grupo = ServiceGrupo(db)
    _grupo = service_grupo.get_grupo(current_user.codigo_grupo)
    grupo = _grupo.nome+' '+_grupo.codigoRegiao+'/'+str(_grupo.codigo)

    service_secao = ServiceSecao(db)
    _secao = service_secao.get_secao(current_user.codigo_secao)
    secao = tipo_secao_str(_secao.codigoTipoSecao)+': '+_secao.nome

    return render_template("index.html",
                           navbar=get_navbar(),
                           user=current_user,
                           panels=panels,
                           grupo=grupo,
                           secao=secao)


def _render_login_mappa():
    # TODO: render_login_mappa
    return render_template("login_mappa.html",
                           user=current_user,
                           page_title="Login MAPPA")


def _render_login():
    return render_template("login_page.html",
                           page_title='Login')


def product(product_id):
    product = Product.query.filter_by(id=product_id).first() or abort(
        404, "produto nao encontrado"
    )
    return render_template("product.html", product=product)
