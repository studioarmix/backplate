
from flask_restful import Resource
from flask import current_app, request, abort, redirect

from webargs import fields
from webargs.flaskparser import use_args

from .actions import auth_facebook

auth_args = {
    'code': fields.String(),
    'ac': fields.String(),
    're': fields.String(),
}

def facebook_auth_endpoint(user_class, refresh_token_class):
    """Returns a flask_restful Resource object for Api use"""

    class FacebookAuthEndpoint(Resource):

        @use_args(auth_args)
        def get(self, args):

            code = args.get('code')

            if code:
                request_uri = request.base_url
                client_id = current_app.config.get('FACEBOOK_CLIENT_ID')
                client_secret = current_app.config.get('FACEBOOK_CLIENT_SECRET')

                res = auth_facebook(
                    code, request_uri, client_id, client_secret,
                    user_class, refresh_token_class)

                request_uri = res.get('request_uri')
                access_token = res.get('access_token')
                refresh_token = res.get('refresh_token')

                token_uri = '{uri}?ac={ac}&re={re}'.format(
                    uri=request_uri, ac=access_token, re=refresh_token)

                return redirect(token_uri, code=302)

            if args.get('ac') and args.get('re'):
                return 'OK'

            return abort(400)

    return FacebookAuthEndpoint
