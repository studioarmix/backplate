
import re
import jwt

from datetime import datetime
from flask import current_app, request

from uuid import uuid4
from hashlib import sha1


def hash(input=None):
    """
    Generate hash from input.

    :param input: (optional) string to hash, defaults to new uuid
    """
    return sha1((input or uuid4().hex).encode()).hexdigest()


def create_refresh_token(refresh_token_class, user_id):
    """
    Commits and returns new refresh token for user with given user id.
    Refresh token is hashed

    :param user_id: id of user to recieve refresh_token session
    """
    token = hash()
    now = datetime.utcnow()

    refresh_token = refresh_token_class(
        user_id=user_id,
        token_hash=hash(token),
        last_update=now
    )

    current_app.db.session.add(refresh_token)
    current_app.db.session.commit()

    return token

def get_refresh_token(refresh_token_class, token):
    """
    Returns a refresh token object.
    """
    token = hash(token)
    return refresh_token_class.query.filter_by(token_hash=token).first()

def delete_refresh_token(refresh_token_class, id):
    """
    Finds and deletes refresh token for user.

    :param id: id of refresh token to delete
    """
    refresh_token = refresh_token_class.query.get(id)
    if refresh_token:
        current_app.db.session.delete(refresh_token)
        current_app.db.session.commit()


def create_access_token(payload):
    """
    Returns a JWT token with the given payload.
    Uses current_app SECRET_KEY for encoding signature.

    :param payload: dictionary containing basic user information
    """
    secret = current_app.config.get('SECRET_KEY')
    life = current_app.config.get('ACCESS_TOKEN_LIFE')
    payload['exp'] = datetime.utcnow() + life
    return jwt.encode(payload, secret, algorithm='HS256').decode()

def parse_access_token(token):
    """
    Validates and returns payload of a given JWT token.
    Uses current_app SECRET_KEY for decoding/checking signature.

    :param token: string of JWT to decode
    """
    secret = current_app.config.get('SECRET_KEY')
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.exceptions.InvalidTokenError:
        return None

    return payload


def get_header_token():
    bearer_re = re.compile(r'Bearer (.+)')

    auth_header = request.headers.get('Authorization')
    if auth_header:
        token_res = bearer_re.match(auth_header)
        if token_res:
            return token_res.group(1)

    return None

def get_url_token():
    return request.args.get('access_token')
