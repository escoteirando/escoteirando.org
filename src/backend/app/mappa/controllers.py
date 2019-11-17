from flask import Blueprint

mappa = Blueprint('mappa', __name__)


@mappa.route('/')
def index():
    return "mAPPa"
