
import sqlalchemy as sa
from marshmallow import Schema, fields


class UserFacebookMixin(object):

    fb_token = sa.Column(sa.Text) # arbitrary length string
    fb_id = sa.Column(sa.String(64)) # numeric string

    fb_email = sa.Column(sa.String(255)) # end@user.com
    fb_name = sa.Column(sa.String(255)) # Full name
    fb_first_name = sa.Column(sa.String(128)) # First name
    fb_last_name = sa.Column(sa.String(128)) # Last name
    fb_locale = sa.Column(sa.String(64)) # en_US, en_UK ...
    fb_gender = sa.Column(sa.String(32)) # male, female, null
    fb_birthday = sa.Column(sa.String(32)) # MM/DD/YYYY
    fb_age_range = sa.Column(sa.String(32)) # MIN-MAX

    def update_from_data(self, data):
        """Update stored information from Facebook User response object"""

        self.fb_email = data.get('email', self.fb_email)
        self.fb_name = data.get('name', self.fb_name)
        self.fb_first_name = data.get('first_name', self.fb_first_name)
        self.fb_last_name = data.get('last_name', self.fb_last_name)
        self.fb_locale = data.get('locale', self.fb_locale)
        self.fb_gender = data.get('gender', self.fb_gender)
        self.fb_birthday = data.get('birthday', self.fb_birthday)

        # age range is returned as a json
        age_range = data.get('age_range')
        if age_range:
            self.fb_age_range = '{}-{}'.format(
                age_range.get('min'),
                age_range.get('max')
            )


class UserFacebookSchema(Schema):

    fb_id = fields.Integer(dump_to='fbId')

    fb_email = fields.String(dump_to='fbEmail')
    fb_name = fields.String(dump_to='fbName')
    fb_first_name = fields.String(dump_to='fbFirstName')
    fb_last_name = fields.String(dump_to='fbLastName')
    fb_locale = fields.String(dump_to='fbLocale')
    fb_gender = fields.String(dump_to='fbGender')
    fb_birthday = fields.String(dump_to='fbBirthday')
    fb_age_range = fields.String(dump_to='fbAgeRange')
