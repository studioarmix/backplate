
from distutils.core import setup

setup(
    name='backbone',
    version='0.1',
    description='RESTful API Helpers',
    author='Peter Boyer',
    author_email='petertboyer@gmail.com',
    url='https://github.com/studioarmix/backbone',
    packages=['backbone'],
    license='MIT',
    install_requires=[
        'flask',
        'flask-restful',
        'flask_cors'
    ]
)
