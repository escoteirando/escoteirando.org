from flask import Blueprint, url_for

import app.start
from app.tools import response

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return "API"


@api.route('/sitemap', methods=["GET"])
def sitemap():
    links = {}
    _app = app.start.app
    for rule in _app.url_map.iter_rules():
        if has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links[url] = {"endpoint": rule.endpoint,
                          "methods": [x for x in rule.methods]}

    return response(links)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
