from uuid import uuid4

from gevent import Greenlet as _Greenlet
from gevent.pool import Group as _Group


class Greenlet(_Greenlet):

    def __init__(self, run=None, *args, **kwargs):
        print self
        super(Greenlet, self).__init__(run, *args, **kwargs)
        self._uuid = str(uuid4())

    @property
    def id(self):
        return self._uuid


class Group(_Group):

    def __init__(self, *args):
        super(Group, self).__init__(*args)
        self._uuid = str(uuid4())

    @property
    def id(self):
        return self._uuid
