
def create_url(url):
    """Provide support for more concise route url definitions

    Convert '/entity/:id' into '/entity/<int:id>'
    Convert '/entity/str:id' into '/entity/<str:id>'
    """

    parts = url.split('/')
    parsed = []
    for part in parts:
        if part.find(':') != -1:
            kind, name = part.split(':')
            parsed.append('<{}:{}>'.format(kind or 'int', name))
        else:
            parsed.append(part)

    return '/{}'.format('/'.join(parsed))


def create_endpoint(url):
    """Provide support for using route urls to generate endpoint definitions

    Convert '/entity' into 'entity-index'
    Convert '/entity/:id' into 'entity-child'
    Convert '/entity/:id/subent' into 'entity-child-subent-index'
    Convert '/entity/:id/subent/:id' into 'entity-child-subent-child'
    """

    parts = url.split('/')
    parsed = []
    for part in parts:
        if part.find(':') != -1:
            parsed.append('child')
        else:
            parsed.append(part)

    if parsed[-1] != 'child':
        parsed.append('index')

    return '-'.join(parsed)


def endpoint(name, url, indexController=None, childController=None, children=[]):
    """Returns a tuple to contruct API routes"""
    return (name, url, indexController, childController, children)


def create_routes(routes):
    """Returns an array of route tuples from potentially nested routes structure"""

    parsed = []

    def parse_routes(_routes, preUrl='', preEnd=''):
        """Recursive routes parsing function to generate endpoints"""

        for route in _routes:
            name, url, indexController, childController, children = route

            url = url[1:] if url.startswith('/') else url

            preUrlIndex = '{}/{}'.format(preUrl, url)
            preUrlChild = '{}/{}/:id'.format(preUrl, url)
            preEndIndex = '{}-{}-index'.format(preEnd, name)
            preEndChild = '{}-{}-child'.format(preEnd, name)

            if preUrlIndex.startswith('/'):
                preUrlIndex = preUrlIndex[1:]
            if preUrlChild.startswith('/'):
                preUrlChild = preUrlChild[1:]
            if preEndIndex.startswith('-'):
                preEndIndex = preEndIndex[1:]
            if preEndChild.startswith('-'):
                preEndChild = preEndChild[1:]
            if not childController:
                preEndIndex = preEndIndex[:-len('-index')]

            parsed.append((preUrlIndex, indexController, preEndIndex))
            if childController:
                parsed.append((preUrlChild, childController, preEndChild))
                parse_routes(children, preUrlChild, preEndChild)
            else:
                parse_routes(children, preUrlIndex, preEndIndex)

    parse_routes(routes)
    return parsed


def add_endpoint(api, url, controller, endpoint=None):
    """Adds an endpoint to given restful_api object"""

    url = create_url(url)
    if not endpoint:
        endpoint = create_endpoint(url)

    return api.add_resource(controller, url, endpoint=endpoint)


def bind_routes(api, routes=[]):
    """From an array of routes binds them to given restful_api object"""

    for route in routes:
        url, controller, endpoint = route
        add_endpoint(api, url, controller, endpoint)
