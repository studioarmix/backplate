# Jumpstart API

Create beautiful Flask-based, RESTful APIs with Jumpstart API's helper methods.

Common account security implementations such as:

- refresh token and access token exchange
- login with Facebook token exchange and user resolution
- more to come.

```bash
$ pip install jumpstartapi
```

## Quickstart

Creating a simple Flask app with the API endpoint at `/api/v1`.

Creates endpoints for `profile` and `business` under the names `/profile` and `/businesses`. Under the hood, the `endpoint()` is registering the endpoint with an indexController for `Businesses` and a childController for `Business`, which is returned by `/businesses` and `/businesses/:id` respectively.

```python
# api.py

from flask import Flask
from jumpstartapi import create_api, endpoint

endpoints = [
    endpoint('profile', '/profile', Profile),
    endpoint('business', '/businesses', Businesses, Business)
]

decorators = [...]

api = create_api('api', __name__, endpoints=endpoints, decorators=decorators)

# __init__.py

from .api import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')
```



## Creating an API with Endpoints

### create_api(name, handle, endpoints=[], decorators=[])

Creates a `flask.Blueprint` using `name` and `handle`.

Creates a `flask_restful.Api` using the blueprint created and the array of `decorators`.

Returns a tuple with the `flask.Blueprint` instance and the `flask_restful.Api` instance, in that order.

Binds `handle_error` and `application/json` presentation logic to the `Api` instance.

Adds `endpoints` through processing the route tuples to form nested routes for the API using the `add_resource` method from the `Api` instance.

### endpoint(name, url, indexController=None, childController=None, children=[])

Creates and returns a tuple for use with `create_api`'s internal route processing and binding.

`name`is a string used to construct an unique endpoint value.

`url` is a string used to define the url name of the resource.

`indexController` expects a class inheriting a `flask_restful` `Resource` object, used for accessing the route when accessed without any child references i.e. `/profile`.

`childController` also expects a `flask_restful#Resource` object, used for accessing the route when accessed with a child id i.e. `/businesses/1`. The `id` passed as the first parameter of the class instance's various response methods e.g. `get(self, id)`, `post(self, id)` etc.

`children` expects a list of  `endpoint` formed tuples that allow for endpoint structures like `/profile/payments` etc.

###Example

```python
# api.py

from jumpstartapi import create_api, endpoint

endpoints = [
    endpoint('profile', '/profile', Profile),
    endpoint('business', '/businesses', Businesses, Business)
]

decorators = [...]

api = create_api(
	'api', __name__,
	endpoints=endpoints,
	decorators=decorators
)
```

## Adding Token API Authentication Flow

When creating your API instance through `create_api` add the `token_auth_required` decorator as a list item for the `decorators` parameter to enforce the API to `401 Unauthorized` abort if:

1. the token is invalid and/or expired
2. the user id referenced by the token can not be found in the database

```python
from jumpstartapi.auth import token_auth_required
from models import User

decorators = [
  	token_auth_required(User)
]
```

### token_auth_required(user_class, ignored_endpoints=[])

Returns a decorator for use with the `Api` instance created with `create_api`.

Adds logic that attempts to retrieve an access token from the HTTP header `Authorization` in the format `Bearer <token>`, or from the url query string value of `access_token`.

The logic then attempts to parse and validate the access token to derive the user id, and then adds the resolved user SQLAlchemy object instance accessible at `g.user`, and the used access token at `g.token`, for the context of the request.

The `user_class` parameter takes a SQLAlchemy queryable declarative class reference.

The `ignored_endpoints` parameter allows specification of endpoint id, which is set by the following pattern when using `create_api` with routes.

### token_renew_endpoint()

Returns a `TokenRenewEndpoint` `flask_restful.Resource` class object for an `endpoint` as an `indexController`.

Provides a `POST` and `DELETE` actions to the specified url e.g. `/token`.

`POST /token?refresh_token=TOKEN`

`DELETE /token?refresh_token=TOKEN`

```python
from jumpstartapi.auth import token_renew_endpoint
from models import RefreshToken

TokenRenewEndpoint = token_renew_endpoint(
    refresh_token_class=RefreshToken)

# ...
endpoints = [
    endpoint('token', '/token', TokenRenewEndpoint)
]
```

### facebook_auth_endpoint()

Returns a `FacebookAuthEndpoint` `flask_restful.Resource` class object for use with an `endpoint` as a controller.

Requires `FACEBOOK_CLIENT_ID` and `FACEBOOK_CLIENT_SECRET` from the Flask app config otherwise requests to the API with raise runtime exceptions.

```python
from jumpstartapi.auth.facebook import facebook_auth_endpoint
from models import User, RefreshToken

FacebookAuthEndpoint = facebook_auth_endpoint(
    user_class=User, refresh_token_class=RefreshToken)

# ...
endpoints = [
	endpoint('auth', '/auth', FacebookAuthEndpoint)
]
```
