# -*- coding: utf-8 -*-

import logging

from flask import (
    Blueprint, Response,
    render_template,
    current_app, g, request,
)
from flask.views import MethodView

from gevent.queue import JoinableQueue, Empty

from socketio import socketio_manage
from socketio.namespace import BaseNamespace

from wtforms import Form, TextField
from werkzeug.local import LocalProxy

from .. import api

__all__ = [
    'build_blueprint',
    'mediasearch',
]


log = logging.getLogger(__name__)


SITE_TITLE = LocalProxy(
    lambda: current_app.config['SITE_TITLE']
)


def build_blueprint():

    mediasearch = Blueprint(
        'mediasearch',
        __name__,
    )

    mediasearch.add_url_rule(
        '/',
        view_func=IndexView.as_view('index'),
    )

    mediasearch.add_url_rule(
        '/socket.io/<path:path>',
        view_func=run_socketio,
    )

    @mediasearch.before_request
    def setup():

        middleware = (
            api.delay_middleware(0.25) if current_app.debug
            else None
        )

        g.api = api.SearchAPI(
            middleware=middleware,
        )

    @mediasearch.teardown_request
    def teardown(*args, **kwargs):

        api = g.get('api', None)
        if api is not None:
            del g.api

    return mediasearch


class SearchForm(Form):
    search_query = TextField('search_query')


class IndexView(MethodView):

    def get(self):

        form = SearchForm()

        return render_template(
            'index.html',
            site_title=SITE_TITLE,
            form=form,
        )


def run_socketio(path):

    real_request = request._get_current_object()
    app = current_app._get_current_object()

    socketio_manage(
        real_request.environ,
        {'/search': MediasearchNamespace},
        request=(real_request, app),
    )

    return Response()


class FlaskNamespace(BaseNamespace):

    """Based on http://flask.pocoo.org/snippets/105/
    Mine seems to actually work, though."""

    def __init__(self, *args, **kwargs):

        # if we pack both real objects inside request
        # we can use them here
        (request, app) = kwargs.get('request', None)

        self.ctx = None

        if request:
            self.ctx = app.request_context(request.environ)
            self.ctx.push()
            app.preprocess_request()

            del kwargs['request']

        super(FlaskNamespace, self).__init__(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        try:
            if self.ctx:
                self.ctx.pop()
        finally:
            super(FlaskNamespace, self).disconnect(*args, **kwargs)


class MediasearchNamespace(FlaskNamespace):

    def initialize(self):

        log.debug('initialize MediasearchNamespace')

    def on_search(self, query):

        log.debug('search for %r', query)

        queue = JoinableQueue()
        task_group = g.api.search(query, queue)

        while True:
            finished = all(
                [t.ready() for t in task_group]
            )
            try:
                item = queue.get(timeout=1.0)
            except Empty:

                if finished:
                    break

                continue

            try:
                self.emit('result', item._asdict())
            finally:
                queue.task_done()

        queue.join()
        task_group.join()

        self.emit('done', query)


mediasearch = build_blueprint()
