
from datetime import datetime
from backplate import Throttle, ThrottlerBase, create_throttler_decorator

database = {}
options = {
    # capacity of bucket (in units)
    'capacity': 5,
    # timeframe for full bucket to empty (in seconds)
    'timeframe': 10
}


class Throttler(ThrottlerBase):
    def get_throttle(self, id):
        if id not in database:
            database[id] = {
                'hits': 0,
                'last': datetime.utcnow()
            }
        return Throttle(obj=database.get(id))

    def set_throttle(self, id, throttle):
        database[id] = throttle.dump()

    def resolve_user_id(self):
        user = {'id': 1}
        return user.get('id')

    def on_throttle_exceed(self, id):
        print('exceeding: {}'.format(id))


throttler = Throttler(**options)
use_throttler = create_throttler_decorator(throttler)

__all__ = ['throttler', 'use_throttler']
