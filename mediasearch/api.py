# -*- coding: utf-8 -*-

from CodernityDB import RecordNotFound, DatabaseConflict

class API(object):

    def __init__(self, db):

        self._db = db

    def search(self, query):

        doc = dict(
            kind='task',
            status='new',
            query=query,
        )

        task = self.db.insert(doc)

        return task

    def poll_task(self):

        doc = next(self.db.all('id'))

        doc['working'] = True

        self.db.insert(doc)


    def poll_results(self, task):

        try:
            doc = self.db.get('id', task['id'])

        except RecordDeleted:
            return []

        if task['_rev'] == doc['_rev']:
            return []





class SearchAPI(object):

    def __init__(self, providers, database):

        self.providers = providers
        self.database = database

    def search(self, query):

        results = itertools.chain(
            p.search(query, self.database) for p in self.providers
        )

        return list(results)

    def search_sync(self, query):

        return []
