# -*- coding: utf-8 -*-

import logging

import requests

from . import SearchResult


log = logging.getLogger(__name__)


class AppleITunesMovies(object):
    """This uses Apple's public web service API."""

    ENDPOINT_URL = u'https://itunes.apple.com/search'
    ENDPOINT_PARAMS_DEFAULT = dict(
        media=u'movie',
    )
    SOURCE = 'iTunes'

    def search(self, query, streaming=False):

        params = dict(
            self.ENDPOINT_PARAMS_DEFAULT,
            term=unicode(query),
        )

        log.debug('requesting %r, %r', self.ENDPOINT_URL, params)

        response = requests.get(self.ENDPOINT_URL, params=params)
        json_data = response.json()

        log.debug('got response, transforming')

        results = self.transform_result(json_data)

        return (
            results if streaming
            else list(results)
        )

    @classmethod
    def transform_result(cls, json_data):

        results = json_data['results']

        log.debug('found %r items in results', len(results))

        return (
            SearchResult(r['trackName'], r['trackViewUrl'], cls.SOURCE)
            for r in results
        )
