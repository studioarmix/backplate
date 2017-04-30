
from distutils.core import setup

setup(
    name='jumpstartapi',
    version='0.1',
    description='RESTful API Jumpstart Utilities',
    author='Peter Boyer',
    author_email='petertboyer@gmail.com',
    url='https://github.com/studioarmix/jumpstart-api',
    packages=['jumpstartapi'],
    license='MIT',
    install_requires=[
        'flask',
        'flask-restful',
        'sqlalchemy',
        'requests',
        'marshmallow',
        'webargs',
        'pyjwt'
    ]
)
