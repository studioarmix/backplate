
from distutils.core import setup

setup(
    name='jumpstartapi',
    version='1.0',
    description='StudioArmix RESTful API Startup Utils',
    author='Peter Boyer',
    author_email='petertboyer@gmail.com',
    url='https://github.com/studioarmix/jumpstart-api',
    packages=[
        'flask',
        'flask-restful',
        'requests',
        'marshmallow',
        'webargs',
        'pyjwt'
    ]
)
