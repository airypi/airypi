import os
from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name = "airypi",
    version = "0.0.1",
    description = "The server libraries for airypi",
    long_description=(read('README.md')),
    url = "https://www.airypi.com/docs/",
    license = "Apache License (2.0)",
    author = "airypi",
    author_email = "dev@airypi.com",
    packages=find_packages(exclude=['tests*']),
    keywords = ["raspberry", "pi", 'server', 'cloud', 'library', 'airypi', 'control', 'io', 'gpio', 'serial', 'smbus', 'spi', 'i2c'],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires = ['Flask',
                        'Flask-OAuthlib',
                        'Flask-SocketIO',
                        'Jinja2',
                        'MarkupSafe',
                        'Werkzeug',
                        'gevent',
                        'gevent-socketio',
                        'gevent-websocket',
                        'greenlet',
                        'itsdangerous',
                        'oauthlib',
                        'redis',
                        'requests',
                        'wsgiref']
)