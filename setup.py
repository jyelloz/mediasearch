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
        'mediasearch.web',
        'mediasearch.testsuite',
    ],
    test_suite='mediasearch.testsuite',
    include_package_data=True,
    entry_points=dict(
        console_scripts=[
            'mediasearch-manage = mediasearch.manage:main',
        ],
    ),
    setup_requires=[
        'nose>=1.0',
        'coverage',
        'wheel',
    ],
    install_requires=[
        'setuptools',
        'Flask',
        'Flask-Failsafe',
        'Flask-Script',
        'WTForms',
        'gevent >= 1.0, >= master-1.0dev, >= 1.0dev',
        'gevent-socketio >= master-0.3.6',
        'requests',
        'lxml',
        'cssselect',
    ],
)
