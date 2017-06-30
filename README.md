# Backplate API
Create beautiful Flask-based, RESTful APIs with Backplate's API helper methods.

## Features
- Simple endpoint generation helpers.
- JSON error formatting helpers for application exceptions.
- Basic response data/error enveloping.

```bash
$ pip install backplate
```

## Quickstart
Creating a simple Flask RESTful API app prefixed with `/v1`.

- Creates endpoints for `me` and `item` under the names `/me` and `/items`
- Endpoints such as `items` can have:
  - indexController (`/items`) and,
  - childController (`/items/:id`).

```python
# example.py

from flask import Flask
from flask_restful import Resource
from backplate import create_api, endpoint

class Profile(Resource):
    # /v1/me
    def get(self):
        return {'id': 1}

class Items(Resource):
    # /v1/items
    def get(self):
        return [{'id': idx} for idx in range(0, 20)]

class Item(Resource):
    # /v1/items/:id
    def get(self, id):
        return {'id': id}

endpoints = [
    endpoint('me', '/me', Profile),
    endpoint('item', '/items', Items, Item)
]

app = Flask(__name__)
create_api(__name__, app=app, endpoints=endpoints)

if __name__ == '__main__':
    app.run()

```

## Error Handling
Passing `errors` parameter into `backplate.create_api()` enables for a consistent error handling experience.

```python
# example.py

from backplate import APIError, errordef

# ...

ERR_TEAPOT = 'ERR_TEAPOT'

errors = [
    errordef(ERR_TEAPOT, 418, 'I am a custom error.')
]

# ...

class Item(Resource):
    def get(self, id):
        # raise custom error
        raise APIError(ERR_TEAPOT, data={
            'fields': {'random': 'Incorrect anything.'}})

# ...

create_api(..., errors=errors)

# ...
```

The `<backplate.APIError>` constructor takes `code`, and optional arguments `status`, and `description`.

The `code` argument is used to match an error created by `backplate.errordef()` in the `errors` array (which is converted into a dict/map internally), and then (using the pre-defined `errors` map as a fallback) generates and formats an appropriate error response with HTTP status code.

Raising an error like `raise APIError(ERR_TEAPOT)` will then be formatted and completed to use the fallback `code` and `description` values provided in the `errors` array that was passed to the `backplate.create_api()` method.

Errors do not need to be defined in the `errors` array to be raised.


## Backplate API Documentation

### backplate.create_api(handle, ...)
Creates API objects for app.

Returns tuple `[<flask.Blueprint>, <flask_restful.Api>]`.

#### Parameters

##### `handle: string`
`flask.Blueprint` constructor `handle` argument.

##### `app?: <flask.Flask>`
Optional reference to `flask.Flask` object instance to bind with.

##### `endpoints?: array<tuple> = []`
Array of tuples generated from the `backplate.endpoint()` helper.

##### `decorators?: array<function> = []`
`flask_restful.Api` constructor `decorators` argument.

##### `prefix?: string = '/v1'`
String for url prefix of all endpoint urls.

##### `name?: string = 'api'`
`flask.Blueprint` constructor `name` argument.

##### `errors?: array<dict> = []`
Array of objects generated from the `backplate.errordef()` helper.

##### `mediatypes?: dict = {}`
Dictionary of media types with key as string e.g. `application/json` and value as function that takes `data, status, headers=[]` and returns `flask.Response` object instance.

By default the `application/json` media type is added if no custom media types are specified, therefore specifying your own would require manually defining `application/json` into the dict.

```python
from backplate import (
    create_json_output_handler,
    format_json_response
)

json_formatter = format_json_response
json_output_handler = create_json_output_handler(json_formatter)

mediatypes = {
    'application/json': json_output_handler,
    # ... other media type definitions
}
```

##### `error_handler?: (e: <Exception>) => <flask.Response>`
Function to override default `error_handler`, which is the result of `backplate.create_error_handler`.

##### `json_output_handler?: (data: any, status: int, headers?: array<string>) => <flask.Response>`
Function to override default `json_output_handler`, which is the result of `backplate.create_json_output_handler`. If manually specifying the `mediatypes` parameter, this override will not be effective.

##### `json_formatter?: (data: any, code: int) => dict`
Function to override the default `json_formatter` function that is passed into the `error_handler` and `json_output_handler` creator methods.

If specifying a custom `error_handler` or `json_output_handler`, this override will not be effective for the respective handler. Furthermore, if manually specifying the `mediatypes` parameter, this override will not be effective for the `json_output_handler`.

#### Functionality
1. Creates a `flask.Blueprint` using `name` and `handle`.
1. Creates a `flask_restful.Api` using the array of `decorators`.
1. Injects `error_handler` into `flask_restful.Api.handle_error` method.
1. Enables `catch_all_404s`.
1. Registers all media type representations from `mediatypes`.
1. Registers all processed routes with blueprint from `endpoints` using `flask_restful.Api.add_resource` method.
1. Binds the blueprint with the `app` using the `url_prefix`.
1. Adds CORS origins headers, defaulting with `*`.
1. Injects `error_handler` into `flask.Flask.handle_bad_request` method of `app`, using `<Exception>` to handle everything.
1. Returns tuple.

### backplate.endpoint(name, url, ...)
Creates tuples for use with `<backplate.create_api>` internal route processing and binding.

#### Parameters

##### `name: string`
Unique name for endpoint node; used to generate resource endpoint paths.

##### `url: string`
Unique url path name with leading `/`, e.g. `'/items'`.

##### `index_controller?: <flask_restful.Resource>`
Expects a class inheriting a `<flask_restful.Resource>` object, used for accessing the route when accessed without any child references i.e. `/items`.

##### `child_controller?: <flask_restful.Resource>`
Also expects a class inheriting a `<flask_restful.Resource>` object, used for when the route is accessed with a child id i.e. `/items/1`.

The `id` passed as the a parameter of the class instance's various response methods e.g. `get(self, id)`, `post(self, id)` etc. and for nested routes is passed as parameters in parent to leaf order.

##### `children?: array<tuple> = []`
An array of child endpoints generated with `backplate.endpoint()`, to allow for nesting url structures, e.g. `/items/:id/attachments`.

##### `child_type?: string = 'int'`
A reference to the type of argument to expect from, of either `int` or `string`.
