from json import dumps

from flask import Response, request
from flask_api import status


def response(data: dict, status: int = status.HTTP_200_OK) -> Response:
    if isinstance(data, str):
        data = {'message': data}

    return Response(dumps(data), status=status, mimetype="application/json")


def request_value(name: str):
    if name in request.form:
        return request.form[name]
    if name in request.values:
        return request.values[name]
    return None


def request_values(names: list):
    values = []
    for name in names:
        values.append(request_value(name))
    return values
