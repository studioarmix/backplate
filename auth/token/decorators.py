
from functools import wraps

from flask import request, abort, g

from .methods import get_header_token, get_url_token, parse_access_token

def trim_api_name_endpoint(endpoint):

    endpoint_parts = endpoint.split('.')
    if len(endpoint_parts) == 1:
        return endpoint

    return ''.join(endpoint_parts[1:])

def token_auth_required(user_class, ignored_endpoints=[]):
    """
    Attempts to find access token from url or header.
    If provided adds token and user object to g context.
    If not provided looks through ignored_endpoints to determine
    whether or not to stop further access of any routes.
    """

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):

            g.token = None
            g.user = None

            # check if the endpoint is ignored, continue if cond
            request_endpoint = trim_api_name_endpoint(request.url_rule.endpoint)
            for endpoint in ignored_endpoints:
                if endpoint.startswith(request_endpoint):
                    return f(*args, **kwargs)

            # attempt to get auth from header, fallback to url
            access_token = get_header_token() or get_url_token()

            # if token is provided validate and add to context
            if access_token:

                data = parse_access_token(access_token)
                if not data:
                    return abort(401)

                user_id = int(data.get('id')) or None
                user = user_class.query.get(user_id)
                if not user:
                    return abort(401)

                g.token = access_token
                g.user = user

            else:

                # not access_token on a auth required endpoint
                return abort(401)

            return f(*args, **kwargs)

        return wrapped
    return wrapper
