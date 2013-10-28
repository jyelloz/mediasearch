#!/usr/bin/env python

from setuptools import setup

setup(
    name='Mediasearch',
    version='0.1',
    license='BSD',
    url='https://jordan.yelloz.me/',
    author='Jordan Yelloz',
    author_email='jordan@yelloz.me',
    description='Searches multiple search providers for media',
    long_description='Searches multiple search providers for media',
    platforms='any',
    packages=[
        'mediasearch',
        'mediasearch.providers',
    ],
    test_suite='mediasearch.testsuite',
    include_package_data=True,
    install_requires=[
        'setuptools',
        'nose',
        'Flask',
        'Flask-Failsafe',
        'Flask-Script',
        'Flask-WTF',
        'Flask-SQLAlchemy',
        'SQLAlchemy',
        'Whoosh',
        'gevent',
        'requests',
        'lxml',
        'cssselect',
    ],
)
