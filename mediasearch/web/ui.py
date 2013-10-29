import logging
from uuid import uuid4

from flask import (
    Blueprint,
    render_template, json,
    current_app, g,
)
from flask.views import MethodView

from wtforms import Form, TextField
from werkzeug.local import LocalProxy

from .. import database


log = logging.getLogger(__name__)


SITE_TITLE = LocalProxy(
    lambda: current_app.config['SITE_TITLE']
)

DATABASE_PATH = LocalProxy(
    lambda: current_app.config['DATABASE']
)


def get_session_searches(session):

    return None


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
        '/api/search',
        view_func=SearchView.as_view('search_query'),
    )

    mediasearch.add_url_rule(
        '/api/search/<query_id>',
        view_func=SearchView.as_view('search_results'),
    )

    @mediasearch.before_app_first_request
    def initialize_database():

        database.initialize(DATABASE_PATH)

    @mediasearch.before_request
    def setup_database():

        g.db = database.connect(DATABASE_PATH)

    @mediasearch.teardown_request
    def teardown_database(*args, **kwargs):

        db = getattr(g, 'db', None)
        db_close = (
            None if db is None
            else db.close
        )
        if db_close is not None:
            db_close()

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


class SearchView(MethodView):

    def post(self, search_query):

        return json.jsonify(
            query_id=uuid4().hex,
        )

    def get(self, query_id):

        return json.jsonify(
            query_id=query_id,
            results=[],
        )


def fake_task():

    from gevent import spawn
    from itertools import chain
    from ..providers.googleplay import GooglePlayMovies
    from ..providers.appleitunes import AppleITunesMovies

    google_play = GooglePlayMovies()
    apple_itunes = AppleITunesMovies()

    google_play_results = spawn(
        lambda: [
            dict(title=title, url=url, source='googleplay')
            for (title, url) in google_play.search('terminator')
        ]
    )

    apple_itunes_results = spawn(
        lambda: [
            dict(title=title, url=url, source='itunes')
            for (title, url) in apple_itunes.search('terminator')
        ]
    )

    results = chain(apple_itunes_results.get(), google_play_results.get())

    for r in results:
        log.info(repr(r))

    print 'done'


mediasearch = build_blueprint()
