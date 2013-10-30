# -*- coding: utf-8 -*-

from gevent import spawn, sleep
from gevent.pool import Group

from .providers.appleitunes import AppleITunesMovies
from .providers.googleplay import GooglePlayMovies

__all__ = [
    'SearchAPI'
]


class SearchAPI(object):

    DEFAULT_PROVIDERS = (
        AppleITunesMovies,
        GooglePlayMovies,
    )

    def __init__(self, providers=None, middleware=None):

        self._providers = (
            providers if providers is not None
            else [p() for p in self.DEFAULT_PROVIDERS]
        )

        self._middleware = (
            middleware if middleware is not None
            else identity_middleware
        )

    def search(self, query, queue):
        """Schedules a search and returns the related task information."""

        group = Group()

        for provider in self._providers:
            group.add(
                spawn(
                    self._search_wrapper,
                    provider,
                    query,
                    queue,
                    self._middleware,
                )
            )

        return group

    @staticmethod
    def _search_wrapper(provider, query, queue, middleware):

        results = provider.search(query, streaming=True)

        for result in middleware(results):
            queue.put(result)


identity_middleware = lambda x: x


def delay_middleware(delay_seconds):

    def wrapper(results):
        for result in results:
            sleep(delay_seconds)
            yield result

    return wrapper
