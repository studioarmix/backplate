
from flask_restful import Resource


class Profile(Resource):
    # /v1/me
    def get(self):
        return {'id': 1}
