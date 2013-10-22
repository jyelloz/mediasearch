import itertools


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
