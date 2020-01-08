from flask import abort, render_template
from escoteirando.models import Product
from flask_simplelogin import is_logged_in
from flask_login import current_user, AnonymousUserMixin, UserMixin
from escoteirando.ext.logging import get_logger
from escoteirando.ext.jinja_tools import get_navbar, get_login_navbar
logger = get_logger()


def index():
    if current_user.is_anonymous:
        return _render_login()
    
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


def _render_login():
    return render_template("login_page.html",
                           navbar=get_login_navbar(),
                           page_title='Login')


def product(product_id):
    product = Product.query.filter_by(id=product_id).first() or abort(
        404, "produto nao encontrado"
    )
    return render_template("product.html", product=product)
