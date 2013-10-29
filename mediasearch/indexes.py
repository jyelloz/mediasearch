# -*- coding: utf-8 -*-

from CodernityDB.hash_index import HashIndex


class SearchTaskIndex(HashIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = 'I'
        super(SearchTaskIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        return key

    def make_key_value(self, data):

        kind = data.get('kind', None)
        if kind != 'task':
            return

        return int(True), None


class SearchTaskStatusIndex(HashIndex):

    def __init__(self, *args, **kwargs):
        task_status = kwargs.pop('task_status')
        kwargs['key_format'] = 'I'
        super(SearchTaskStatusIndex, self).__init__(*args, **kwargs)

        self.task_status = task_status

    def make_key(self, key):
        return key

    def make_key_value(self, data):

        kind = data.get('kind', None)
        if kind != 'task':
            return

        status = data.get('status', None)
        if status != self.task_status:
            return

        return int(True), None


class SearchResultIndex(HashIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(SearchResultIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        return key

    def make_key_value(self, data):

        kind = data.get('kind', None)
        if kind != 'result':
            return

        return bytes(data['task_id']), None
