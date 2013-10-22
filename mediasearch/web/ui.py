from flask import (
    Blueprint,
    render_template, url_for,
    current_app, session, request, g,
)
from flask.views import MethodView

from flask.ext.wtf import Form
from wtforms import TextField
from werkzeug.local import LocalProxy


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

    return mediasearch


class IndexView(MethodView):

    class SearchForm(Form):
        search_query = TextField('search_query')

    def get(self):

        form = self.SearchForm()

        return render_template(
            'index.html',
            site_title=site_title,
            form=form,
            form_url=url_for('.index'),
        )

    def post(self):

        form = self.SearchForm()

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
