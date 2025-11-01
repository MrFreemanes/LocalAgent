from unittest import TestCase, main
from unittest.mock import Mock, MagicMock, patch, call

from core.vectorizers.vectorizer import Vectorizer


class VectorizerTest(TestCase):
    def setUp(self):
        self.base_path = 'C:/User'

        self.file_1 = {'path': 'AppData/text.txt', 'hash': 'abc', 'mtime': 10.32}
        self.file_2 = {'path': 'AppData/data.dat', 'hash': 'qwe', 'mtime': 4.57}
        self.files_db = MagicMock()
        self.files_db.get_unindexed_files.return_value = [self.file_1, self.file_2]
        self.files_db.update.return_value = None

        self.vector_db = MagicMock()
        self.vector_db.add.return_value = None

        self.model = MagicMock()
        self.model.embed.return_value = [[-0.0735117495059967, -0.1563340276479721, -0.7277779579162598]]

        self.vectorizer = Vectorizer(self.files_db, self.vector_db, self.model, self.base_path)
        self.vectorizer.logger = MagicMock()

    def test_run_total_is_zero(self):
        self.files_db.get_unindexed_files.return_value = []

        run = self.vectorizer.run()

        self.assertEqual(next(run), 100)
        self.assert_stop_iteration(run)

        self.assertEqual(self.vectorizer.logger.debug.call_args[0][0], 'Все файлы уже имеют вектора.')

    @patch('core.vectorizers.vectorizer.read_file_to_chunks')
    def test_run(self, read_file_to_chunks_mock):
        read_file_to_chunks_mock.return_value = ['text_1', 'text_2']
        run = self.vectorizer.run()

        called = (
            call(
                path=self.file_1['path'],
                mtime=self.file_1['mtime'],
                hash_=self.file_1['hash'],
                indexed=1
            ),
            call(
                path=self.file_2['path'],
                mtime=self.file_2['mtime'],
                hash_=self.file_2['hash'],
                indexed=1
            )
        )

        self.assertEqual(next(run), 50)

        self.assertEqual(
            self.vector_db.add.call_args[0][0:3],
            (self.file_1['path'], 1, 'text_2')
        )

        self.assertEqual(next(run), 100)

        self.assertEqual(
            self.vector_db.add.call_args[0][0:3],
            (self.file_2['path'], 1, 'text_2')
        )

        self.assert_stop_iteration(run)

        self.files_db.update.assert_has_calls(called)

        self.assertEqual(self.vectorizer.logger.debug.call_args[0][0], 'Векторизация завершена.')

    @patch('core.vectorizers.vectorizer.read_file_to_chunks', side_effect=TypeError('Не строка'))
    def test_run_except(self, read_file_to_chunks_mock):
        self.files_db.get_unindexed_files.return_value = [self.file_1]

        run = self.vectorizer.run()

        self.assertEqual(next(run), 100)
        self.assert_stop_iteration(run)

        self.assertEqual(
            self.vectorizer.logger.error.call_args[0][0:2],
            ('Ошибка при обработке %s: %s', self.file_1['path'])
        )

        self.assertEqual(
            self.vectorizer.logger.error.call_args[0][2].__class__,
            TypeError().__class__
        )

        self.assertEqual(self.vectorizer.logger.debug.call_args[0][0], 'Векторизация завершена.')

    def assert_stop_iteration(self, generator):
        with self.assertRaises(StopIteration):
            next(generator)


if __name__ == '__main__':
    main()
