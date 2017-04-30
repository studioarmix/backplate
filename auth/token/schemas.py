
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr

class RefreshTokenMixin(object):

    __tablename__ = 'user_refresh_token'

    id = sa.Column(sa.Integer, primary_key=True)

    token_hash = sa.Column(sa.String(1024))
    last_update = sa.Column(sa.DateTime)

    @declared_attr
    def user_id(cls):
        return sa.Column(sa.Integer, sa.ForeignKey('user.id'))

    @declared_attr
    def user(cls):
        return sa.orm.relationship('User')


class UserRefreshTokenMixin(object):

    @declared_attr
    def refresh_tokens(cls):
        return sa.orm.relationship(
            'RefreshToken',
            primaryjoin='RefreshToken.user_id == {}.id'.format(
                cls.__name__))
