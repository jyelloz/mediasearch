# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

import logging
import unittest

from random import random
from urlparse import urlunsplit

from gevent import Greenlet, sleep, spawn
from gevent.event import Event
from gevent.pool import Group
from gevent.queue import JoinableQueue, Empty

from mediasearch.providers import SearchResult


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Service(object):

    def search(self, query, streaming=False):

        query_lower = query.lower()

        results = (
            SearchResult(v, self.url(i), self.SOURCE)
            for (i, v) in enumerate(self.VIDEOS)
            if query_lower in v.lower()
        )

        return (
            results if streaming
            else list(results)
        )

    def url(self, id):

        video_url = urlunsplit((
            'https',
            self.NETLOC,
            '/video/{id}'.format(id=id),
            None,
            None,
        ))

        return unicode(video_url)


class FirstService(Service):

    VIDEOS = [
        'Das Boot',
        'The Cable Guy',
        'Terminator',
        'Terminator 2',
        'Videodrome',
    ]
    SOURCE = 'First Service'
    NETLOC = 'firstservice.example.com'


class SecondService(Service):

    VIDEOS = [
        'Melancholia',
        'Terminator 3',
        'The Jerk',
    ]
    SOURCE = 'Second Service'
    NETLOC = 'secondservice.example.com'


class ThirdService(Service):

    VIDEOS = [
        'American Ninja 2',
        'Bloodsport',
        'Police Academy 4',
        'Terminator',
    ]
    SOURCE = 'Third Service'
    NETLOC = 'thirdservice.example.com'


class GreenletTestcase(unittest.TestCase):

    def setUp(self):
        pass

    def test_greenlet(self):

        queue = JoinableQueue()
        requests_done = Event()

        g = Greenlet(self._producer, queue, FirstService(), 'Terminator')
        h = Greenlet(self._producer, queue, SecondService(), 'Terminator')
        i = Greenlet(self._producer, queue, ThirdService(), 'Terminator')

        requests = Group()

        for request in g, h, i:
            requests.add(request)

        log.debug('before spawn')

        c = spawn(
            self._consumer,
            done=requests_done,
            queue=queue,
        )
        [r.start() for r in requests]

        log.debug('after spawn')

        requests.join()
        requests_done.set()

        log.debug('requests are done')

        c.join()

        log.debug('consumer is done')

    @staticmethod
    def _consumer(done, queue):

        log.debug('waiting for results')

        while not done.is_set():

            try:
                result = queue.get(timeout=1)
            except Empty:
                continue

            try:
                log.debug('received %r', result)
            finally:
                queue.task_done()

    @staticmethod
    def _producer(queue, service, query):

        results = service.search(query, streaming=True)

        for result in results:

            delay = 5 * random()

            log.debug(
                '%s: sleeping for %0.2f seconds',
                service.SOURCE,
                delay,
            )
            sleep(delay)

            queue.put(result)

        log.debug(
            'done producing results from %r',
            service,
        )
