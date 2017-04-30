
import sqlalchemy as sa
from marshmallow import Schema, fields

from flask import current_app


class UserMixin(object):

    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    deactivated = sa.Column(sa.Boolean, default=False)


class UserSchema(Schema):

    id = fields.Integer()


class UserTokenSchema(UserSchema):
    class Meta:
        fields = ('id', )


def get_facebook_user(cls, id, data={}, token=None):
    """
    Gets or Creates a User object from given Facebook data.

    :param id: Facebook User profile ID
    :param data: (optional) Dictionary of attributes to update User object
    :param token: (optional) Facebook access_token to update User object
    """

    user = cls.query.filter_by(fb_id=id).first()
    if not user:
        user = cls()
        user.fb_id = id
        current_app.db.session.add(user)

    if token:
        user.fb_token = token
    if data:
        user.update_from_data(data)

    current_app.db.session.commit()

    return user
