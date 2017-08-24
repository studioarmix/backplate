
import re
import logging

from flask import jsonify, current_app

log = logging.getLogger(__name__)

_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')

def to_snake_case(s):
    subbed = _underscorer1.sub(r'\1_\2', s)
    return _underscorer2.sub(r'\1_\2', subbed).lower()

class APIException(Exception):
    def __init__(self,
                 status=None,
                 code=None,
                 message=None,
                 data=None):

        self.status = status
        self.code = code
        self.message = message
        self.data = data

    def format(self):
        error_object = {
            'code': self.code,
            'status': self.status,
            'message': self.message,
        }

        if self.data:
            error_object['data'] = self.data

        return error_object

class Error:
    def __init__(self,
                 status=400,
                 code=None,
                 exception=None,
                 message=None):

        self.status = status

        self.code = code
        self.exception = exception
        self.message = message

def create_error_handler(errors={}, json_formatter=None):

    error_code_map = {}
    error_exception_map = {}

    for error in errors:
        if error.code:
            error_code_map[error.code] = error
        if error.exception:
            error_exception_map[error.exception] = error

    def handle_error(e):
        error = None

        # get exception status code, default 500 for unknown/generic
        code = to_snake_case(str(type(e).__name__)).upper()
        status = getattr(e, 'code', 500)
        message = str(e)
        data = getattr(e, 'data', None)

        e_type = type(e)
        if e_type is APIException:
            # ready
            error = e

        else:
            # set error from exception map
            error = error_exception_map.get(e_type)

            # fallback to bases of the class
            if not error:
                for base in e_type.__bases__:
                    if base in error_exception_map:
                        error = error_exception_map.get(base)
                        break

            # default to generic exceptions
            if not error:
                if ':' in message and len(message.split(' ')[0].strip()) == 3:
                    status = int(message.split(' ')[0].strip())
                    code = message[3:message.index(':')] \
                        .strip()
                    code = '{}_{}'.format(status, code) \
                        .replace(' ', '_').upper()
                    message = message[message.index(':') + 1:] \
                        .strip()

        code = (error and error.code) or code
        status = (error and error.status) or status
        message = (error and error.message) or message
        e = APIException(status, code, message, data)

        if error:
            e.status = e.status or error.status
            e.message = e.message or error.message

        # log exception if 500 server error
        # remove message for consumer facing data if not on DEBUG mode
        status = e.status
        if status >= 500:
            log.exception(e)
            if current_app.config.get('DEBUG') is not True:
                e.message = None

        # json formatter for data envelopes
        data = e.format()
        if callable(json_formatter):
            data = json_formatter(data, status)

        resp = jsonify(data)
        return resp, status
    return handle_error

__all__ = ['APIException', 'Error']
