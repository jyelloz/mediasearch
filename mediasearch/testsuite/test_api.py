from unittest import TestCase as _TestCase


class Database(object):

    def __init__(self):

        self.data = dict()

    def put(self, key, value):

        self.data[key] = value

    def get(self, key, default=None):

        return self.data.get(key, default)


class FakeProvider(object):

    DATA = {
        'some terms': 'a document with some terms',
    }

    def search(self, terms, database):

        from uuid import uuid4

        query_pk = str(uuid4())
        result = self.DATA.get(terms, None)

        database.put(query_pk, result)

        return query_pk


class SearchAPITestcase(_TestCase):

    def setUp(self):

        from mediasearch.api import SearchAPI

        self.database = database = Database()
        self.api = SearchAPI([FakeProvider()], database)

    def tearDown(self):

        setattr(self, 'api', None)

    def test_search(self):

        sub_results = self.api.search('some terms')

        result = [self.database.get(pk) for pk in sub_results]

        print sub_results
        print result
