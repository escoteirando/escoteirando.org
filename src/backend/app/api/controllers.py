from flask import Blueprint, request

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return "API"
