# Backplate Documentation

### Creators

#### `create_api(handle, ...)`

```python
from backplate import create_api
```

Creates API objects for app, and if passed `app` argument, will return app with bound handlers, otherwise returns tuple `[flask.Blueprint, flask_restful.Api]`.

- `handle: string`
  `flask.Blueprint` constructor `handle` argument.

- `app?: flask.Flask`
  Optional reference to `flask.Flask` object instance to bind with.

- `endpoints?: array<tuple> = []`
  Array of tuples generated from the `backplate.endpoint()` helper.

- `decorators?: array<callable> = []`
  `flask_restful.Api` constructor `decorators` argument.

- `prefix?: string = '/v1'`
  String for url prefix of all endpoint urls.

- `name?: string = 'api'`
  `flask.Blueprint` constructor `name` argument.

- `errors?: array<dict> = []`
  Array of objects generated from the `backplate.errordef()` helper.

- `mediatypes?: dict = {}`
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

- `error_handler?: (e: Exception) => flask.Response`
  Function to override default `error_handler`, which is the result of `backplate.create_error_handler`.

- `json_output_handler?: (data: any, status: int, headers?: array<string>) => flask.Response`
  Function to override default `json_output_handler`, which is the result of `backplate.create_json_output_handler`. If manually specifying the `mediatypes` parameter, this override will not be effective.

- `json_formatter?: (data: any, code: int) => dict`
  Function to override the default `json_formatter` function that is passed into the `error_handler` and `json_output_handler` creator methods.
  If specifying a custom `error_handler` or `json_output_handler`, this override will not be effective for the respective handler. Furthermore, if manually specifying the `mediatypes` parameter, this override will not be effective for the `json_output_handler`.

- **Returns**
  Returns the passed `app` object instance, otherwise returns a newly constructed Flask app instance.



##### Functionality
1. Creates a `flask.Blueprint` using `name` and `handle`.
2. Creates a `flask_restful.Api` using the array of `decorators`.
3. Injects `error_handler` into `flask_restful.Api.handle_error` method.
4. Enables `catch_all_404s`.
5. Registers all media type representations from `mediatypes`.
6. Registers all processed routes with blueprint from `endpoints` using `flask_restful.Api.add_resource` method.
7. Binds the blueprint with the `app` using the `url_prefix`.
8. Adds CORS origins headers, defaulting with `*`.
9. Injects `error_handler` into `flask.Flask.handle_bad_request` method of `app`, using `Exception` to handle everything.
10. Returns tuple.



### Definition Helpers

### `Route(name, url, ...)`

```python
from backplate import Route
```

Creates tuples for use with `backplate.create_api` internal route processing and binding.

- `name: string`
  Unique name for Route node; used to generate resource Route paths.
- `url: string`
  Unique url path name with leading `/`, e.g. `'/items'`.
- `index_controller?: flask_restful.Resource`
  Expects a class inheriting a `flask_restful.Resource` object, used for accessing the route when accessed without any child references i.e. `/items`.
- `child_controller?: flask_restful.Resource`
  Also expects a class inheriting a `flask_restful.Resource` object, used for when the route is accessed with a child id i.e. `/items/1`.
  The `id` passed as the a parameter of the class instance's various response methods e.g. `get(self, id)`, `post(self, id)` etc. and for nested routes is passed as parameters in parent to leaf order.
- `children?: array<tuple> = []`
  An array of child endpoints generated with `backplate.Route()`, to allow for nesting url structures, e.g. `/items/:id/attachments`.
- `child_type?: string = 'int'`
  A reference to the type of argument to expect from, of either `int` or `string`.
- **Returns**
  A tuple of values intended to be used in an array passed to `backplate.create_api`.



### `Error(code, ...)`

```python
from backplate import Error
```

Creates dict objects for use with `backplate.create_api` internal error processing.

- `code: string`
  Unique code that will remain constant and consistent for clients to consume. Using this code in an `backplate.APIException` constructor will use all properties further defined below as a fall-back and provide a consistent error reporting experience.
- `status?: int = 400`
  HTTP status code that will be used by default when reporting this error.
- `message?: string = None`
  Optional descriptive human readable text about the error of which the client should not depend upon as it may change.
- `exception?: Exception = None`
  Optional reference to an Exception type that the error code will bind to in the event that the API raises it in a response. If `message` is not defined the string representation of the Exception will populate the `message` field for an error response.
- **Returns**
  A dict intended to be used in an array passed to `backplate.create_api`.



### Exceptions

```python
from backplate import APIException
```

The base exception object that is constructed with additonal data attributes to describe an API error with contextual HTTP terms.

- `code: string`
  Unique code that preferably refers to a previously defined `Error()` that has been passed into the `create_api()` function. If the `code` has been registered with the API a response will fall-back to those values, however these can be overridden with contextual information by defining the properties further defined below.
- `status?: int = 400`
  HTTP status code to be used in the response.
- `message? string = None`
  Optional descriptive human readable text about the error.
- `data? any = None`
  Any additional data e.g. per-field error messages, to be included in the response error object.

