# -*- coding: utf-8 -*-

import logging

from unittest import TestCase
from httmock import urlmatch, with_httmock

from mediasearch.providers.googleplay import GooglePlayMovies
from mediasearch.providers.appleitunes import AppleITunesMovies
from mediasearch.providers.netflix import NetflixMovies

from . import TESTSUITE_BASEDIR

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


@urlmatch(netloc=r'^play.google.com$')
def load_googleplay_terminator(url, request):

    from os.path import join

    path = join(
        TESTSUITE_BASEDIR,
        'data',
        'test_googleplay_terminator.html',
    )

    with open(path, 'rb') as f:
        content = f.read()

    return dict(
        status_code=200,
        content=content,
    )


@urlmatch(netloc=r'^itunes.apple.com$')
def load_appleitunes_terminator(url, request):

    from os.path import join

    path = join(
        TESTSUITE_BASEDIR,
        'data',
        'test_appleitunes_terminator.json',
    )

    with open(path, 'rb') as f:
        content = f.read()

    return dict(
        status_code=200,
        content=content,
    )


@urlmatch(netloc=r'^(\S+\.)?netflix.com$')
def load_netflix_terminator(url, request):

    from os.path import join

    path = join(
        TESTSUITE_BASEDIR,
        'data',
        'test_netflix_terminator.xml',
    )

    with open(path, 'rb') as f:
        content = f.read()

    return dict(
        status_code=200,
        content=content,
    )


class ProvidersTestcase(TestCase):

    QUERY = 'terminator'

    @with_httmock(load_googleplay_terminator)
    def test_googleplay_movies(self):

        provider = GooglePlayMovies()

        result = provider.search(self.QUERY)

        self.assertEqual(len(result), 25)

    @with_httmock(load_appleitunes_terminator)
    def test_appleitunes_movies(self):

        provider = AppleITunesMovies()

        result = provider.search(self.QUERY)

        self.assertEqual(len(result), 6)

    @with_httmock(load_netflix_terminator)
    def test_netflix_movies(self):

        provider = NetflixMovies()

        result = provider.search(self.QUERY)

        # not implemented yet
        self.assertEqual(len(result), -1)
