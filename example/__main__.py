
from backplate import create_api, Route

from endpoints import Profile, Items, Item
from errors import errors
from throttler import use_throttler

routes = [
    Route('me', '/me', Profile),
    Route('item', '/items', Items, Item)
]

decorators = [
    use_throttler
]

app = create_api(
    __name__,
    routes=routes,
    decorators=decorators,
    errors=errors
)

if __name__ == '__main__':
    app.run(debug=True)
