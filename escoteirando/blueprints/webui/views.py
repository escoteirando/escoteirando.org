from flask import abort, render_template
from escoteirando.models import Product
from flask_simplelogin import is_logged_in


def index():
    if is_logged_in():
        return _render_index()
    else:
        return _render_login()


def _render_index():
    products = Product.query.all()
    return render_template("index.html", products=products)


def _render_login():
    return render_template('login_form.html')


def product(product_id):
    product = Product.query.filter_by(id=product_id).first() or abort(
        404, "produto nao encontrado"
    )
    return render_template("product.html", product=product)
