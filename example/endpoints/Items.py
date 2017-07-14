
from flask_restful import Resource
from backplate import APIError
from errors import ERR_TEAPOT

class Items(Resource):
    # /v1/items
    def get(self):
        return [{'id': idx} for idx in range(0, 20)]

class Item(Resource):
    # /v1/items/:id
    def get(self, id):
        if id > 20:
            raise APIError(ERR_TEAPOT, data={
                'fields': {'random': 'Incorrect anything.'}})
        return {'id': id}
