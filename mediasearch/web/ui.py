from flask import (
    Blueprint,
    render_template, url_for,
    current_app, session, g,
)
from flask.views import MethodView

from flask.ext.wtf import Form
from wtforms import TextField
from werkzeug.local import LocalProxy

from CodernityDB.database_thread_safe import ThreadSafeDatabase


site_title = LocalProxy(
    lambda: current_app.config['SITE_TITLE']
)

session_searches = LocalProxy(lambda: get_session_searches(session))


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
        '/search',
        view_func=SearchView.as_view('search'),
    )

    mediasearch.add_url_rule(
        '/search/<query>',
        view_func=SearchView.as_view('search_query'),
    )

    @mediasearch.before_request
    def setup_database():

        g.db = db = ThreadSafeDatabase(
            current_app.config['DATABASE']
        )

        db.exists() and db.open() or db.create()

    @mediasearch.teardown_request
    def teardown_database(*args, **kwargs):

        db = getattr(g, 'db', None)
        if db is not None:
            db.close()

    return mediasearch


class SearchForm(Form):
    search_query = TextField('search_query')


class IndexView(MethodView):

    def get(self):

        from gevent import spawn_later

        form = SearchForm()

        current_app.logger.debug('scheduling fake task')
        spawn_later(5, self.fake_task)

        return render_template(
            'index.html',
            site_title=site_title,
            form=form,
            form_url=url_for('.search'),
        )

    def fake_task(self):

        from gevent import sleep

        print 'running fake task'

        sleep(5)

        print 'done'


class SearchView(MethodView):

    def get(self):

        form = SearchForm()

        return render_template(
            'search.html',
            site_title=site_title,
            form=form,
            form_url=url_for('.search'),
        )

    def post(self):

        form = SearchForm()

        if not form.validate_on_submit():
            return render_template(
                'index.html',
                site_title=site_title,
                form=form,
                form_url=url_for('.index'),
            )

        search_query = form.data['search_query']

        return 'searched for %r' % search_query


mediasearch = build_blueprint()
