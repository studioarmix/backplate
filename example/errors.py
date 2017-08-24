
from backplate import Error

class CustomTeabagError(Exception):
    pass

ERR_TEAPOT = 'ERR_TEAPOT'
ERR_TEABAG = 'ERR_TEABAG'

errors = [
    # error from APIError
    Error(ERR_TEAPOT, 418, 'I am a custom error.'),
    # catch raised exception CustomTeabagError
    Error(CustomTeabagError, 419, code=ERR_TEABAG)
]
