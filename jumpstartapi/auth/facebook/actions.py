
from .methods import get_access_token, get_profile
from ..token.methods import create_refresh_token, create_access_token
from ...user import UserTokenSchema, get_facebook_user

def auth_facebook(code, request_uri,
                  client_id=None, client_secret=None,
                  user_class=None, refresh_token_class=None):
    """
    Using Facebook OAuth Code:
    - request access token
    - create user if Facebook id is not in DB with User
    - return refresh_token and access_token JWT for Republic API

    :param code: security code string from Facebook API to exchange
                 into an access_token that can be used for queries
    """

    if not code:
        raise RuntimeError('Invalid code')

    # request Access Token container from Facebook
    token = get_access_token(code, request_uri, client_id, client_secret)
    if not token:
        raise RuntimeError('Facebook failed to respond with access token data')

    # pull Access Token from response container
    access_token = token.get('access_token')
    # get User profile from Facebook using Access Token
    profile = get_profile(access_token)

    if not profile:
        raise RuntimeError('Facebook failed to respond with profile data')

    profile_id = profile.get('id')

    # internally find User by response id, otherwise create a new object
    user = get_facebook_user(user_class, profile_id, profile, access_token)

    # create new refresh token for session
    refresh_token = create_refresh_token(refresh_token_class, user.id)
    # create new access token for session
    access_token = create_access_token(UserTokenSchema().dump(user).data)

    return dict(
        request_uri=request_uri,
        access_token=access_token,
        refresh_token=refresh_token)
