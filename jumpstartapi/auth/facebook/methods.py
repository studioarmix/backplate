
import requests

user_fields = [
    'email', 'name', 'first_name', 'last_name',
    'locale', 'gender', 'birthday', 'age_range'
]

graph_api_uri = ('https://graph.facebook.com/v2.8')

access_token_uri = (
    graph_api_uri + '/oauth/access_token'
    '?client_id={client_id}'
    '&client_secret={client_secret}'
    '&code={code}'
    '&redirect_uri={redirect_uri}'
)

profile_uri = (
    graph_api_uri + '/me'
    '?access_token={access_token}'
    '&fields=' + (','.join(user_fields))
)

entity_uri = (
    graph_api_uri + '/{entity_id}'
    '?access_token={access_token}'
    '&fields=' + (','.join(user_fields))
)


def graph_api_request(url):

    request = requests.get(url)

    response = request.json()
    if not response:
        return None

    if not request.status_code == 200:
        raise RuntimeError('Facebook - {}'.format(
            response.get('error', {}).get('message')))

    return response


def get_access_token(code, redirect_uri, client_id=None, client_secret=None):
    """Exchange Facebook OAuth Code for Access Token"""

    return graph_api_request(access_token_uri.format(
        code=code,
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=client_secret,
    ))


def get_profile(access_token):
    """Request Facebook Profile information using Access Token"""

    return graph_api_request(profile_uri.format(
        access_token=access_token
    ))


def get_entity(entity_id, access_token):
    """Request Facebook Entity (i.e. User) using id and Access Token"""

    return graph_api_request(entity_uri.format(
        entity_id=entity_id,
        access_token=access_token
    ))
