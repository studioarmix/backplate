
import logging

from flask import Blueprint, jsonify
from flask_restful import Api

from .routing import bind_routes, create_routes

log = logging.getLogger(__name__)


def format_response(data, code):

    if code < 400:
        resp = {'data': data}
    else:
        resp = {'error': {'code': code}}
        if type(data) is str:
            resp['error']['message'] = data
        else:
            resp['error']['errors'] = data

    return resp


def output_json(data, code, headers=None):

    data = format_response(data, code)
    resp = jsonify(data)
    resp.status_code = code
    resp.headers.extend(headers)

    return resp


def handle_error(e):

    messages = {
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        410: 'Gone',
        500: 'Internal Server Error',
        503: 'Service Unavailable'
    }

    code = getattr(e, 'code', 500)
    data = format_response(str(e) or messages[code], code)
    resp = jsonify(data)

    if code == 500:
        log.exception(e)

    return resp, code


def create_api(name, handle, endpoints=[], decorators=[]):
    """Returns flask blueprint and restful_api object from args"""

    bp = Blueprint(name, handle)

    class _Api(Api):
        def handle_error(self, e):
            return handle_error(e)

    api = _Api(bp, decorators=decorators)
    api.catch_all_404s = True
    api.representation('application/json')(output_json)

    bind_routes(api, create_routes(endpoints))

    return bp, api
