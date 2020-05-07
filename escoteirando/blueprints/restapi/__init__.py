from flask import Blueprint
from flask_restful import Api

from .auth import auth
from .mappa import mappa_bp
from .notificacoes import setup_notificacoes
from .resources import ProductItemResource, ProductResource

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app):
    setup_notificacoes(api)
    api.add_resource(ProductResource, "/product/")
    api.add_resource(ProductItemResource, "/product/<product_id>")
    app.register_blueprint(bp)
    app.register_blueprint(auth)
    app.register_blueprint(mappa_bp)
