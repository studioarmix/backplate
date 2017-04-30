
from flask_restful import Resource
from flask import abort

from webargs import fields
from webargs.flaskparser import use_args

from .actions import (
    auth_refresh_token as auth_refresh_token_action,
    deauth_refresh_token as deauth_refresh_token_action,
)

def auth_refresh_token(refresh_token_class, token):

    access_token = auth_refresh_token_action(refresh_token_class, token)
    if access_token:
        return {
            'access_token': access_token
        }

    return abort(400)

def deauth_refresh_token(refresh_token_class, token):

    deauth_refresh_token_action(refresh_token_class, token)
    return 'OK'


auth_args = {
    'refresh_token': fields.String(),
    'deauth': fields.String()
}

def token_renew_endpoint(refresh_token_class):

    class TokenRenewEndpoint(Resource):

        @use_args(auth_args)
        def post(self, args):

            refresh_token = args.get('refresh_token')
            if refresh_token:
                return auth_refresh_token(refresh_token_class, refresh_token)

            return abort(400)

        @use_args(auth_args)
        def delete(self, args):

            refresh_token = args.get('refresh_token')
            if refresh_token:
                return deauth_refresh_token(refresh_token_class, refresh_token)

            return abort(400)

    return TokenRenewEndpoint
