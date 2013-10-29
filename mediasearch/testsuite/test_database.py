import logging

from tempfile import mkdtemp
from unittest import TestCase as _TestCase

from mediasearch import database

log = logging.getLogger(__name__)


class DatabaseTestcase(_TestCase):

    def setUp(self):

        logging.basicConfig(level=logging.DEBUG)

        self.directory = directory = mkdtemp()
        database.initialize(directory)
        self.db = database.connect(directory)

    def test_task_status_index(self):

        db = self.db

        self.assertEqual(
            list(db.all('search_task_new')),
            list(),
        )

        self.assertEqual(
            list(db.all('search_task_working')),
            list(),
        )

        abc = db.insert(dict(
            kind='task',
            status='new',
            query='abc',
        ))

        self.assertEqual(
            len(list(db.all('search_task_new'))),
            1,
        )

        abc_id = abc['_id']

        abc_new = db.get('id', abc_id)

        abc_new['status'] = 'working'
        db.update(abc_new)

        self.assertEqual(
            list(db.all('search_task_new')),
            list(),
        )

        self.assertEqual(
            len(list(db.all('search_task_working'))),
            1,
        )

        abc_working = db.get('id', abc_id)
        abc_working['status'] = 'done'
        db.update(abc_working)

        self.assertEqual(
            list(db.all('search_task_new')),
            list(),
        )

        self.assertEqual(
            list(db.all('search_task_working')),
            list(),
        )

        self.assertEqual(
            len(list(db.all('search_task_done'))),
            1,
        )

    def test_type_indexes(self):

        db = self.db

        self.assertEqual(
            list(db.all('search_result')),
            list(),
        )

        self.assertEqual(
            list(db.all('search_task')),
            list(),
        )

        abc = dict(
            kind='task',
            status='new',
            query='abc',
        )

        abc_doc = db.insert(abc)
        abc_id = abc_doc['_id']

        self.assertEqual(
            len(list(db.all('search_task'))),
            1,
        )

        self.assertEqual(
            list(db.all('search_result')),
            list(),
        )

        defgh = dict(
            kind='result',
            title='DEFGH',
            url='http://localhost/',
            source='some source',
            task_id=abc_id,
        )

        db.insert(defgh)

        self.assertEqual(
            len(list(db.all('search_result'))),
            1,
        )

    def tearDown(self):

        self.db.destroy()
        log.info('deleted database in %r', self.db.path)
