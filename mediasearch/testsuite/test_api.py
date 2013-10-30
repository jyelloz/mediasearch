# -*- coding: utf-8 -*-

import logging

from unittest import TestCase as _Testcase
from httmock import with_httmock

from gevent import monkey
from gevent.queue import JoinableQueue, Empty

from mediasearch.api import SearchAPI

from .test_providers import (
    load_googleplay_terminator,
    load_appleitunes_terminator,
    load_netflix_terminator,
)


monkey.patch_all()
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class APITestcase(_Testcase):

    def setUp(self):

        self.api = SearchAPI()

    @with_httmock(
        load_googleplay_terminator,
        load_appleitunes_terminator,
        load_netflix_terminator,
    )
    def test_api(self):

        queue = JoinableQueue()
        task_group = self.api.search('terminator', queue)

        while True:
            finished = all(
                [greenlet.ready() for greenlet in task_group.greenlets]
            )
            try:
                item = queue.get(timeout=1.0)
            except Empty:

                if finished:
                    log.info('queue is empty and all jobs are done, quitting')
                    break

                log.info(
                    'queue was empty and jobs are still running, retrying'
                )

                continue

            try:
                log.info('%r', item)
            finally:
                queue.task_done()

        task_group.join()
        queue.join()

        log.info('joined everything')
