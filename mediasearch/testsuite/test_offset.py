# -*- coding: utf-8 -*-

import logging
import unittest

from offset import go, maintask, makechan, run
from offset.time import sleep, SECOND
from offset.sync.waitgroup import WaitGroup

from mediasearch.providers.googleplay import GooglePlayMovies
from mediasearch.providers.appleitunes import AppleITunesMovies


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class OffsetTestcase(unittest.TestCase):

    def setUp(self):
        pass

    def test_offset(self):

        wait = WaitGroup()
        channel = makechan()

        def go_wait(func, *args, **kwargs):
            wait.add(1)
            go(func, *args, **kwargs)

        def search(provider, term):

            print 'searching with %r' % provider

            results = provider.search(term, streaming=True)

            for result in results:
                channel.send(result)
                sleep(SECOND)

            print 'done searching with %r' % provider
            wait.done()

        @maintask
        def main():

            play = GooglePlayMovies()
            itunes = AppleITunesMovies()

            go_wait(search, play, 'terminator')
            go_wait(search, itunes, 'terminator')

            while wait.counter > 0:
                result = channel.recv()
                print 'received %r' % result._asdict()

            wait.wait()

        run()
