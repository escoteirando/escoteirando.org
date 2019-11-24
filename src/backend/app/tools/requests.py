from json import dumps

from flask import Response, request
from flask_api import status


def response(data: dict, status: int = status.HTTP_200_OK) -> Response:
    if isinstance(data, str):
        data = {'message': data}

    return Response(dumps(data), status=status, mimetype="application/json")


def request_values(*names):
    values = []
    for name in names:
        if name in request.form:
            values.append(request.form[name])
        elif name in request.values:
            values.append(request.values[name])
        else:
            values.append(None)

    return values
