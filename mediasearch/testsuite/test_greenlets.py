# -*- coding: utf-8 -*-

import logging
import pickle
import unittest

from datetime import datetime
from random import random
from uuid import uuid4

from gevent import Greenlet, monkey, sleep
from gevent.event import AsyncResult, Event
from gevent.pool import Group

from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, Text
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


monkey.patch_all()
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Service(object):

    def search(self, query):

        return [
            v for v in self.VIDEOS
            if query in v
        ]


class FirstService(Service):

    VIDEOS = [
        'Das Boot',
        'The Cable Guy',
        'Terminator',
        'Terminator 2',
        'Videodrome',
    ]


class SecondService(Service):

    VIDEOS = [
        'Melancholia',
        'Terminator 3',
        'The Jerk',
    ]


class ThirdService(Service):

    VIDEOS = [
        'American Ninja 2',
        'Bloodsport',
        'Police Academy 4',
        'Terminator',
    ]


Base = declarative_base()


class SearchResult(Base):

    __tablename__ = 'search_result'

    pk = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )
    search_pk = Column(
        String(255),
        nullable=False,
    )
    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    source = Column(
        Text,
        nullable=False,
    )
    data = Column(
        LargeBinary,
        nullable=False,
    )


class GreenletTestcase(unittest.TestCase):

    def setUp(self):

        self.engine = engine = create_engine('sqlite:///test.db.sqlite3')
        self.session_factory = session_factory = sessionmaker(bind=engine)
        self.Session = scoped_session(session_factory)

        Base.metadata.create_all(engine)

    def test_greenlet(self):

        requests_done = Event()
        callbacks_done = Event()

        def a(event, service, query, search_pk):

            session = self.Session()

            result = service.search(query)

            delay = 0.25 + (random())

            source = str(service.__class__.__name__).lower()
            log.debug('%s: sleeping for %0.2f seconds', source, delay)
            sleep(delay)

            r = [
                SearchResult(
                    search_pk=search_pk,
                    data=pickle.dumps(item),
                    source=source,
                ) for item in result
            ]
            session.add_all(r)
            session.commit()

            event.set(r[0].timestamp)

            self.Session.remove()

        last_consumed = [0]

        def b(event, search_pk, delay=0):

            log.debug('waiting for results for search_pk %r', search_pk)

            sleep(delay)

            if callbacks_done.is_set():
                log.debug('all responses are consumed, skipping')
                return

            if requests_done.is_set():
                log.debug(
                    'requests have been completed, this is the last callback'
                )
                callbacks_done.set()

            latest = event.get()

            session = self.Session()

            result = session.query(SearchResult).filter(
                SearchResult.pk > last_consumed[0],
                SearchResult.search_pk == search_pk,
            )

            items = list(result.all())
            count = len(items)

            last_consumed[0] = max([i.pk for i in items] + last_consumed)

            log.info(
                'got %d results for search_pk %r',
                count,
                search_pk,
            )

            for item in items:
                data = pickle.loads(item.data)
                log.info('[%s] %s: %r', str(latest), item.source, data)

            self.Session.remove()

        search_pk = str(uuid4())

        ge = AsyncResult()
        he = AsyncResult()
        ie = AsyncResult()

        g = Greenlet(a, ge, FirstService(), 'Terminator', search_pk)
        h = Greenlet(a, he, SecondService(), 'Terminator', search_pk)
        i = Greenlet(a, ie, ThirdService(), 'Terminator', search_pk)

        gc = Greenlet(b, ge, search_pk, 5)
        hc = Greenlet(b, he, search_pk, 2.5)
        ic = Greenlet(b, ie, search_pk, 0.1)

        requests = Group()
        callbacks = Group()

        [requests.add(request) for request in [g, h, i]]
        [callbacks.add(callback) for callback in [gc, hc, ic]]

        log.debug('before spawn')

        [c.start() for c in callbacks]
        [r.start() for r in requests]

        log.debug('after spawn')

        requests.join()
        requests_done.set()
        callbacks.join()

        log.debug('everything is done')
