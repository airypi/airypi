import os
from setuptools import setup

setup(
    name = "airypi",
    version = "0.0.1",
    author = "airypi",
    author_email = "support@airypi.com",
    description = ("The server libraries for airypi"),
    license = "Apache License (2.0)",
    keywords = ["raspberry", "pi", 'server', 'cloud', 'library', 'airypi', 'control', 'io', 'gpio', 'serial', 'smbus', 'spi', 'i2c'],
    url = "http://packages.python.org/airypi",
    packages=['airypi'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
    ],
)