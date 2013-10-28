import requests


class AppleITunes(object):

    ENDPOINT_URL = 'https://itunes.apple.com/search'
    ENDPOINT_PARAMS_DEFAULT = dict(
        media=u'movie',
    )

    def search(self, query):

        params = dict(
            self.ENDPOINT_PARAMS_DEFAULT,
            term=unicode(query),
        )

        response = requests.get(self.ENDPOINT_URL, params=params)
