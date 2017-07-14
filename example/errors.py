
from backplate import errordef

class CustomTeabagError(Exception):
    pass

ERR_TEAPOT = 'ERR_TEAPOT'
ERR_TEABAG = 'ERR_TEABAG'

errors = [
    # error from APIError
    errordef(ERR_TEAPOT, 418, 'I am a custom error.'),
    # catch raised exception CustomTeabagError
    errordef(ERR_TEABAG, 419, exception=CustomTeabagError)
]
