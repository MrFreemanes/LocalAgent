from unittest import TestCase, main
from unittest.mock import Mock, patch

from data.db import vector_db


class VectorDBTest(TestCase):
    _path = 'C:/Program Files/vectors.db'

    @patch('data.db.vector_db.sqlite3')
    def test_connect(self, sqlite3_mock):
        connect = vector_db.VectorDB.connect

        self_mock = Mock()
        self_mock.path_db = r'C:/Program Files'
        self_mock.logger = Mock()

        db_mock = Mock()
        sqlite3_mock.connect.return_value = db_mock
        sqlite3_mock.Row = 'Row'

        connect(self_mock)

        sqlite3_mock.connect.assert_called_once_with(self._path)
        self.assertEqual(self_mock._conn.row_factory, 'Row')
        self.assertEqual(
            self_mock.logger.debug.call_args[0],
            ('[VectorDB] db открыта: %s', self._path)
        )

    def test_create_tables(self):
        create_tables = vector_db.VectorDB._create_tables

        self_mock = self.get_base_self_mock()

        create_tables(self_mock)

        sql = self_mock._conn.execute.call_args[0][0]
        self.assertIn('CREATE TABLE IF NOT EXISTS vectors', sql)
        self.assertEqual(self_mock._conn.commit.call_count, 1)

    @patch('data.db.vector_db.json')
    @patch('data.db.vector_db.time')
    def test_add(self, time_mock, json_mock):
        add = vector_db.VectorDB.add

        self_mock = self.get_base_self_mock()
        self_mock.logger = Mock()
        time_mock.time.return_value = 123.456
        json_mock.dumps.return_value = '[1, 2, 3]'

        add(self_mock, 'C:/file.txt', 0, 'chunk text', [1, 2, 3])

        sql = self_mock._conn.execute.call_args[0][0]
        args = self_mock._conn.execute.call_args[0][1]

        self.assertIn('INSERT INTO vectors', sql)
        self.assertEqual(args[0], 'C:/file.txt')
        self.assertEqual(args[1], 0)
        self.assertEqual(args[2], 'chunk text')
        self.assertEqual(args[3], '[1, 2, 3]')
        self.assertEqual(args[4], 123.456)
        self.assertEqual(self_mock._conn.commit.call_count, 1)

    @patch('data.db.vector_db.json')
    @patch('data.db.vector_db.time')
    def test_update(self, time_mock, json_mock):
        update = vector_db.VectorDB.update

        self_mock = self.get_base_self_mock()
        self_mock.logger = Mock()
        time_mock.time.return_value = 999.999
        json_mock.dumps.return_value = '["v"]'

        update(self_mock, 'C:/f.txt', 1, 'new text', [0.1])

        sql = self_mock._conn.execute.call_args[0][0]
        args = self_mock._conn.execute.call_args[0][1]

        self.assertIn('UPDATE vectors', sql)
        self.assertEqual(args[0], 'new text')
        self.assertEqual(args[1], '["v"]')
        self.assertEqual(args[2], 999.999)
        self.assertEqual(args[3], 'C:/f.txt')
        self.assertEqual(args[4], 1)
        self.assertEqual(self_mock._conn.commit.call_count, 1)

    def test_get_vectors_by_file(self):
        get_vectors_by_file = vector_db.VectorDB.get_vectors_by_file

        cur_mock = Mock()
        cur_mock.fetchall.return_value = [{'id': 1}]

        self_mock = self.get_base_self_mock()
        self_mock._conn.execute.return_value = cur_mock

        result = get_vectors_by_file(self_mock, 'C:/file.txt')

        self.assertIn('SELECT * FROM vectors', self_mock._conn.execute.call_args[0][0])
        self.assertEqual(self_mock._conn.execute.call_args[0][1][0], 'C:/file.txt')
        self.assertEqual(result, [{'id': 1}])

    def test_delete_vectors_by_file(self):
        delete_vectors_by_file = vector_db.VectorDB.delete_vectors_by_file

        self_mock = self.get_base_self_mock()
        self_mock.logger = Mock()

        delete_vectors_by_file(self_mock, 'C:/file.txt')

        sql = self_mock._conn.execute.call_args[0][0]
        args = self_mock._conn.execute.call_args[0][1]

        self.assertIn('DELETE FROM vectors', sql)
        self.assertEqual(args[0], 'C:/file.txt')
        self.assertEqual(self_mock._conn.commit.call_count, 1)
        self.assertEqual(
            self_mock.logger.debug.call_args[0],
            ('[VectorDB] Удалены векторы для %s', 'C:/file.txt')
        )

    @staticmethod
    def get_base_self_mock():
        self_mock = Mock()
        self_mock._conn = Mock()
        self_mock._conn.execute.return_value = None
        self_mock._conn.commit.return_value = None
        return self_mock


if __name__ == '__main__':
    main()
