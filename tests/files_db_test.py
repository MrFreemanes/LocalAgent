from unittest import TestCase, main
from unittest.mock import Mock, patch

from data.db import files_db


class FileDBTest(TestCase):
    _path = 'C:/Program Files/files.db'

    @patch('data.db.files_db.sqlite3')
    def test_connect(self, sqlite3_mock):
        connect = files_db.FileDB.connect

        self_mock = Mock()
        self_mock._path_db = r'C:/Program Files'
        self_mock._conn = Mock()
        self_mock.logger = Mock()

        db_mock = Mock()

        sqlite3_mock.connect.return_value = db_mock
        sqlite3_mock.Row = 'Row'
        connect(self_mock)

        sqlite3_mock.connect.assert_called_once_with(self._path)
        self.assertEqual(self_mock._conn.row_factory, 'Row')

        self.assertEqual(self_mock.logger.debug.call_args[0], ('db открыта: %s', self._path))

    def test_create_tables(self):
        create_tables = files_db.FileDB._create_tables

        self_mock = self.get_base_self_mock()

        create_tables(self_mock)

        self.assertIn('CREATE TABLE IF NOT EXISTS files', self_mock._conn.execute.call_args[0][0])
        self.assertEqual(self_mock._conn.commit.call_count, 1)

    def test_get_file_by_path(self):
        get_file_by_path = files_db.FileDB.get_file_by_path

        cur_mock = Mock()
        cur_mock.fetchone.return_value = {'path': self._path}

        self_mock = self.get_base_self_mock()
        self_mock._conn.execute.return_value = cur_mock

        result = get_file_by_path(self_mock, self._path)

        self.assertEqual(self_mock._conn.execute.call_args[0][1][0], self._path)
        self.assertEqual(result, cur_mock.fetchone.return_value)

    def test_add(self):
        add = files_db.FileDB.add

        self_mock = self.get_base_self_mock()

        add(self_mock, self._path, 1.1, 'qwe')

        self.assertIn('INSERT INTO files', self_mock._conn.execute.call_args[0][0])
        self.assertEqual(self_mock._conn.commit.call_count, 1)

    def test_update(self):
        update = files_db.FileDB.update

        self_mock = self.get_base_self_mock()

        update(self_mock, self._path, 1.1, 'qwe')

        self.assertIn('UPDATE', self_mock._conn.execute.call_args[0][0])
        self.assertEqual(self_mock._conn.commit.call_count, 1)

    def test_get_unindexed_files(self):
        get_unindexed_files = files_db.FileDB.get_unindexed_files

        cur_mock = Mock()
        cur_mock.fetchall.return_value = [(1, 2), (3, 4)]

        self_mock = self.get_base_self_mock()
        self_mock._conn.execute.return_value = cur_mock

        result = get_unindexed_files(self_mock)

        self.assertEqual(result, cur_mock.fetchall.return_value)

    @staticmethod
    def get_base_self_mock():
        self_mock = Mock()
        self_mock._conn.commit.return_value = None
        self_mock._conn.execute.return_value = None
        return self_mock


if __name__ == '__main__':
    main()
