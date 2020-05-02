from flask import Blueprint
from .docs import get_privacidade, get_termos
docs = Blueprint("docs", __name__, url_prefix="/docs/v1")

docs.add_url_rule("/privacidade", view_func=get_privacidade)
docs.add_url_rule("/termos", view_func=get_termos)


def init_app(app):
    app.register_blueprint(docs)
