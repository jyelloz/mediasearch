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


class SearchTaskStatusNewIndex(HashIndex):

    KIND = 'task'
    TASK_STATUS = 'new'

    def __init__(self, *args, **kwargs):

        kwargs['key_format'] = 'I'
        super(SearchTaskStatusNewIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        return key

    def make_key_value(self, data):

        kind = data.get('kind', None)
        status = data.get('status', None)
        if kind != self.KIND or status != self.TASK_STATUS:
            return

        return int(True), None


class SearchTaskStatusWorkingIndex(HashIndex):

    KIND = 'task'
    TASK_STATUS = 'working'

    def __init__(self, *args, **kwargs):

        kwargs['key_format'] = 'I'
        super(SearchTaskStatusWorkingIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        return key

    def make_key_value(self, data):

        kind = data.get('kind', None)
        status = data.get('status', None)
        if kind != self.KIND or status != self.TASK_STATUS:
            return

        return int(True), None


class SearchTaskStatusDoneIndex(HashIndex):

    KIND = 'task'
    TASK_STATUS = 'done'

    def __init__(self, *args, **kwargs):

        kwargs['key_format'] = 'I'
        super(SearchTaskStatusDoneIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        return key

    def make_key_value(self, data):

        kind = data.get('kind', None)
        status = data.get('status', None)
        if kind != self.KIND or status != self.TASK_STATUS:
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
