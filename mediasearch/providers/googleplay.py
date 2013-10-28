import requests


class GooglePlayMovies(object):

    ENDPOINT_URL = 'https://play.google.com/store/search'
    ENDPOINT_PARAMS_DEFAULT = dict(
        c=u'movies',
    )

    def search(self, query):

        params = dict(
            self.ENDPOINT_PARAMS_DEFAULT,
            q=unicode(query),
        )

        response = requests.get(self.ENDPOINT_URL, params=params)
