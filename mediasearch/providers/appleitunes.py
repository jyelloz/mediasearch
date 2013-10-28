import logging

import requests


log = logging.getLogger(__name__)


class AppleITunesMovies(object):
    """This uses Apple's public web service API."""

    ENDPOINT_URL = u'https://itunes.apple.com/search'
    ENDPOINT_PARAMS_DEFAULT = dict(
        media=u'movie',
    )

    def search(self, query):

        params = dict(
            self.ENDPOINT_PARAMS_DEFAULT,
            term=unicode(query),
        )

        log.debug('requesting %r, %r', self.ENDPOINT_URL, params)

        response = requests.get(self.ENDPOINT_URL, params=params)
        json_data = response.json()

        log.debug('got response, transforming')

        return self.transform_result(json_data)

    @classmethod
    def transform_result(cls, json_data):

        results = json_data['results']

        log.debug('found %r items in results', len(results))

        return [
            (r['trackName'], r['trackViewUrl'])
            for r in results
        ]
