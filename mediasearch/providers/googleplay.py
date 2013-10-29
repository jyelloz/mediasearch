# -*- coding: utf-8 -*-

import logging

import requests

from lxml import html
from cssselect import GenericTranslator

from urlparse import urlunsplit, urlsplit


log = logging.getLogger(__name__)


class GooglePlayMovies(object):
    """This uses an XML parser and XPath selectors built from CSS
    selectors to parse Google Play Store movie search results
    since there is no public web service API.
    """

    ENDPOINT_URL = u'https://play.google.com/store/search'
    ENDPOINT_PARAMS_DEFAULT = dict(
        c=u'movies',
    )

    def search(self, query):

        params = dict(
            self.ENDPOINT_PARAMS_DEFAULT,
            q=unicode(query),
        )

        log.debug('requesting %r, %r', self.ENDPOINT_URL, params)

        response = requests.get(self.ENDPOINT_URL, params=params)

        text = response.text

        log.debug('got response, transforming')

        return self.transform_result(text)

    @classmethod
    def transform_result(cls, text):

        translator = GenericTranslator()

        item_xpath = translator.css_to_xpath(
            'div.card.movies a.title'
        )

        document = html.fromstring(text)

        elements = document.xpath(item_xpath)

        log.debug(
            'found %r matching elements for xpath %r',
            len(elements),
            item_xpath,
        )

        def absolutize(path, base=urlsplit(cls.ENDPOINT_URL)):

            return urlunsplit((
                base.scheme,
                base.netloc,
                path,
                '',
                '',
            ))

        items = (
            (e.get('title'), e.get('href'))
            for e in elements
        )

        return [
            (title, absolutize(path)) for
            (title, path) in items
        ]
