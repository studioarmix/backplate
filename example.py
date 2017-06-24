
from backbone import (
    create_api, endpoint,
    APIError, errordef
)

from flask import Flask
from flask_restful import Resource

ERR_FIELDS_INVALID = 'ERR_FIELDS_INVALID'
ERR_EMAIL_ALREADY_EXISTS = 'ERR_EMAIL_ALREADY_EXISTS'
ERR_MY_ERROR = 'ERR_MY_ERROR'

class Profile(Resource):
    def get(self):
        return {
            'id': 1
        }

class Business(Resource):
    def get(self, id):
        if int(id) > 19:
            raise APIError(ERR_MY_ERROR, data={
                'fields': {'username': 'Incorrect length.'}})

        return {
            'id': id
        }

class Businesses(Resource):
    def get(self):
        return [{'id': idx} for idx in range(0, 20)]

endpoints = [
    endpoint('profile', '/profile', Profile),
    endpoint('business', '/businesses', Businesses, Business)
]

decorators = []

errors = [
    errordef(ERR_FIELDS_INVALID,
             422, 'One or more fields raised validation errors.'),
    errordef(ERR_EMAIL_ALREADY_EXISTS,
             409, 'An account already exists with this email.'),
    errordef(ERR_MY_ERROR,
             422, 'My Awesome Error')
]

app = Flask(__name__)

create_api(
    'api', __name__,
    endpoints=endpoints,
    decorators=decorators,
    errors=errors,
    app=app
)

if __name__ == '__main__':
    app.run(debug=True)
