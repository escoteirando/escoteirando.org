import time

from flask import abort, render_template
from flask_login import current_user

from escoteirando.domain.models.user import User, db
from escoteirando.domain.services.infra.service_user import ServiceUser
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
    service_user = ServiceUser(db)
    user = service_user.current_user()
    grupo = "Grupo não identificado"
    secao = "Seção não identificada"

    if user:
        grupo = "{0} {1}/{2}".format(
            user.nom_grupo,
            user.cod_regiao,
            user.cod_grupo)

        secoes = service_user.get_secoes()
        if len(secoes) > 0:
            secao = "{0}: {1}".format(
                secoes[0].tipo_secao_str,
                secoes[0].nome)

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
