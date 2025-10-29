from queue import Queue
from unittest import TestCase, main
from unittest.mock import Mock, MagicMock, patch, call

from core.workers import worker
from config.config import Result, Task, Status


class WorkerModuleTest(TestCase):
    @patch('core.workers.worker.logger')
    @patch('core.workers.worker.initialize')
    @patch('core.workers.worker.vectorization')
    @patch('core.workers.worker.scanning')
    def test_worker(self, scanning_mock, vectorization_mock, initialize_mock, logger_mock):
        task_q, result_q = Queue(), Queue()
        task_q.put(Task('init', 'C:/User'))
        task_q.put(Task('scanning', 'C:/User'))
        task_q.put(Task('vector', 'C:/User'))
        task_q.put(Task('request', 'C:/User', query='Задача'))
        task_q.put(None)

        f_db_mock = MagicMock()
        v_db_mock = MagicMock()
        model_mock = MagicMock()

        initialize_mock.return_value = (f_db_mock, v_db_mock, model_mock)

        worker.worker(task_q, result_q)

        initialize_mock.assert_called_once()
        scanning_mock.assert_called_once()
        vectorization_mock.assert_called_once()
        model_mock.request.assert_called_once()

        f_db_mock.close.assert_called_once()
        v_db_mock.close.assert_called_once()

    @patch('core.workers.worker.logger')
    @patch('core.workers.worker.initialize')
    def test_run_err(self, initialize_mock, logger_mock):
        err = Exception('Ошибка')
        initialize_mock.side_effect = err

        task_q = Queue()
        result_q = Queue()

        task_q.put(Task('init', 'C:/user'))
        task_q.put(None)

        worker.worker(task_q, result_q)

        self.assertEqual(logger_mock.error.call_args[0], ('Ошибка worker: %s', err))

        self.assertEqual(result_q.get(), Result(data={},
                                                status=Status.ERROR,
                                                progress=100,
                                                text_error='Ошибка'))

        self.assertTrue(result_q.empty())

    @patch('core.workers.worker.logger')
    @patch('core.workers.worker.WindowsScanner')
    def test_scanning(self, WindowsScanner_mock, logger_mock):
        gen = self.get_generator()
        scan_mock = MagicMock()
        scan_mock.scan.return_value = gen
        WindowsScanner_mock.return_value = scan_mock

        f_db_mock = MagicMock()
        result_q = Queue()

        worker.scanning('C:/user', f_db_mock, result_q)

        calls = [call('Ошибка: директория не была просканирована'), ] * 2

        self.assertEqual(result_q.get(), Result(data={'worker': 'scanning'},
                                                status=Status.ERROR,
                                                progress=100,
                                                text_error='Ошибка: директория не была просканирована'))
        self.assertEqual(result_q.get(), Result(data={'worker': 'scanning'},
                                                status=Status.ERROR,
                                                progress=100,
                                                text_error='Ошибка: директория не была просканирована'))
        logger_mock.warning.assert_has_calls(calls)
        self.assertEqual(result_q.get(), Result(data={'worker': 'scanning'},
                                                status=Status.RUN,
                                                progress=50))
        self.assertEqual(result_q.get(), Result(data={'worker': 'scanning'},
                                                status=Status.DONE,
                                                progress=100))

    @patch('core.workers.worker.logger')
    @patch('core.workers.worker.Vectorizer')
    def test_vectorization(self, Vectorizer_mock, logger_mock):
        gen = self.get_generator()
        vectorizer_mock = MagicMock()
        vectorizer_mock.run.return_value = gen
        Vectorizer_mock.return_value = vectorizer_mock

        f_db_mock = MagicMock()
        v_db_mock = MagicMock()
        model_mock = MagicMock()

        result_q = Queue()

        worker.vectorization('C:/user', f_db_mock, v_db_mock, model_mock, result_q)

        logger_mock.warning.assert_called_once_with('Ошибка, progress = %s', -1)
        self.assertEqual(result_q.get(), Result(data={'worker': 'vector'},
                                                status=Status.DONE,
                                                progress=100))
        self.assertEqual(result_q.get(), Result(data={'worker': 'vector'},
                                                status=Status.RUN,
                                                progress=50))
        self.assertEqual(result_q.get(), Result(data={'worker': 'vector'},
                                                status=Status.DONE,
                                                progress=100))

    @staticmethod
    def get_generator():
        return_values = [-1, 0, 50, 100]
        for value in return_values:
            yield value


if __name__ == '__main__':
    main()
