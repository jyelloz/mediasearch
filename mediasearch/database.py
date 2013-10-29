# -*- coding: utf-8 -*-

from logging import getLogger

from CodernityDB.database_thread_safe import ThreadSafeDatabase as Database

from . import indexes as i


log = getLogger(__name__)


def initialize(path):

    from os.path import abspath

    db = Database(unicode(path))

    if db.exists():
        db.open()
        db.reindex()
        log.info('loaded existing database at %r', abspath(db.path))
        return

    db.create()

    indexes = [
        i.SearchTaskIndex(
            db.path,
            'search_task',
        ),
        i.SearchResultIndex(
            db.path,
            'search_result',
        ),
        i.SearchTaskStatusNewIndex(
            db.path,
            'search_task_new',
        ),
        i.SearchTaskStatusWorkingIndex(
            db.path,
            'search_task_working',
        ),
        i.SearchTaskStatusDoneIndex(
            db.path,
            'search_task_done',
        ),
    ]

    map(
        db.add_index,
        indexes,
    )

    log.info('initialized database at %r', abspath(db.path))


def connect(path):

    database = Database(unicode(path))

    assert database.exists()

    database.open()

    return database
