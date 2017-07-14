
from flask import Flask
from backplate import create_api, endpoint
from endpoints import Profile, Items, Item
from errors import errors
from throttler import use_throttler

endpoints = [
    endpoint('me', '/me', Profile),
    endpoint('item', '/items', Items, Item)
]

decorators = [
    use_throttler
]

app = create_api(
    __name__,
    app=Flask(__name__),
    endpoints=endpoints,
    decorators=decorators,
    errors=errors
)

if __name__ == '__main__':
    app.run(debug=True)
