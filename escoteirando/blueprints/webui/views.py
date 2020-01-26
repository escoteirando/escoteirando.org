from flask import abort, render_template
from flask_login import current_user

from escoteirando.domain.models.user import User
from escoteirando.ext.jinja_tools import get_login_navbar, get_navbar
from escoteirando.ext.logging import get_logger
from escoteirando.models import Product

logger = get_logger()


def index():
    if current_user.is_anonymous:
        return _render_login()

    user: User = current_user
    if not user.codigo_associado:
        logger.info(user)
        # return _render_login_mappa('')

    # TODO: Verificar o estado do usuario e apresentar a view correspondente
    return _render_index()


def view_test():
    return render_template("login_page.html",
                           navbar=get_login_navbar(),
                           page_title='Login')


def _render_index():
    panels = [
        {"title": "Estatísticas", "url": "#", "id": "stats"},
        {"title": "Últimas atividades", "url": "#", "id": "ult_atv"},
        {"title": "Estatísticas 2 ", "url": "#", "id": "stats"},
        {"title": "Últimas atividades 2", "url": "#", "id": "ult_atv"}
    ]

    return render_template("index.html",
                           navbar=get_navbar(),
                           user=current_user,
                           panels=panels)


def _render_login_mappa():
    # TODO: render_login_mappa
    pass


def _render_login():
    return render_template("login_page.html",
                           # navbar=get_login_navbar(),
                           page_title='Login')


def product(product_id):
    product = Product.query.filter_by(id=product_id).first() or abort(
        404, "produto nao encontrado"
    )
    return render_template("product.html", product=product)
