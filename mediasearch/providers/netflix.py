# -*- coding: utf-8 -*-

import logging


log = logging.getLogger(__name__)


class NetflixMovies(object):
    """Netflix no longer allows new sign-ups to its API"""

    ENDPOINT_URL = u'http://api-public.netflix.com/catalog/titles'
    ENDPOINT_PARAMS_DEFAULT = dict()

    def search(self, query):

        raise NotImplementedError()

    @classmethod
    def transform_result(cls, json_data):

        raise NotImplementedError()
