from uuid import uuid4

from gevent import Greenlet


class TraceableGreenlet(Greenlet):

    def __init__(self, run=None, *args, **kwargs):
        print self
        super(TraceableGreenlet, self).__init__(run, *args, **kwargs)
        self._uuid = str(uuid4())

    @property
    def id(self):
        return self._uuid
