from flask import Blueprint, request, url_for
import app.start
from app.tools import response
api = Blueprint('api', __name__)


@api.route('/')
def index():
    return "API"


@api.route('/sitemap')
def sitemap():
    links = {}
    _app = app.start.app
    for rule in _app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links[url] = rule.endpoint

    return response(links)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
