
from .methods import (
    create_access_token,
    get_refresh_token,
    delete_refresh_token
)

from ...user import UserTokenSchema

def auth_refresh_token(refresh_token_class, token):
    """
    Using Refresh Token from API on initial auth:
    - find refresh token with user
    - return new access_token

    :param token: the refresh token issued on initial auth
    """

    refresh_token = get_refresh_token(refresh_token_class, token)
    if not refresh_token:
        raise RuntimeError('Invalid refresh token')

    user = refresh_token.user
    access_token = create_access_token(UserTokenSchema().dump(user).data)

    return dict(
        user=user,
        access_token=access_token)

def deauth_refresh_token(refresh_token_class, token):
    """
    Using Refresh Token from API on initial auth:
    - find refresh token
    - delete it

    :param token: the refresh token issued on initial auth
    """

    refresh_token = get_refresh_token(refresh_token_class, token)
    if refresh_token:
        delete_refresh_token(refresh_token_class, refresh_token.id)

    return True
