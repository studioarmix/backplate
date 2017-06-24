
from flask import Flask
from flask_restful import Resource
from backplate import create_api, endpoint

class Profile(Resource):
    def get(self):
        return {'id': 1}

class Items(Resource):
    def get(self):
        return [{'id': idx} for idx in range(0, 20)]

class Item(Resource):
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
