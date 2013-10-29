from logging import getLogger

from CodernityDB.database_thread_safe import ThreadSafeDatabase as Database


log = getLogger(__name__)


def initialize(path):

    from os.path import abspath

    db = Database(unicode(path))

    db.exists() or db.create() and log.info(
        'initialized database at %r',
        abspath(db.path),
    )


def connect(path):

    database = Database(unicode(path))

    assert database.exists()

    database.open()

    return database
