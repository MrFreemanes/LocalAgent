from unittest import TestCase, main
from unittest.mock import Mock, patch, call

from core.bridges.bridge import Bridge
from config.config import Result, Status


class BridgeTest(TestCase):
    result_progress = Result({'data': 'text'}, Status.RUN, 56)
    result_done = Result({'data': 'text'}, Status.DONE, 100)
    result_error = Result({'data': 'text'}, Status.ERROR, 13, text_error='Произошла ошибка')
    result_unknown_status = Result({}, 'unknown status', 1)

    def test_handle_result(self):
        handle_result = Bridge._handle_result

        self_mock = Mock()
        self_mock.logger = Mock()
        self_mock.process_signal.emit.return_value = None
        self_mock.done_signal.emit.return_value = None
        self_mock.error_signal.emit.return_value = None

        handle_result(self_mock, self.result_progress)
        handle_result(self_mock, self.result_done)
        handle_result(self_mock, self.result_error)
        handle_result(self_mock, self.result_unknown_status)

        # test signal_progress, signal_done
        self_mock.process_signal.emit.assert_called_once_with(self.result_progress)
        self_mock.done_signal.emit.assert_called_once_with(self.result_done)

        # test signal_error
        self.assertEqual(self_mock.error_signal.emit.call_count, 2)
        calls_signal_error = [
            call(self.result_error.text_error),
            call(f'Статус не определен: {self.result_unknown_status.status}')
        ]
        self_mock.error_signal.emit.assert_has_calls(calls_signal_error)

        # test logging
        calls_debug = [
            call('Получен промежуточный результат: %s', self.result_progress.progress),
            call('Получен конечный результат: %s', self.result_done.__repr__())
        ]
        self_mock.logger.debug.assert_has_calls(calls_debug, any_order=False)
        calls_warning = [
            call('Ошибка в вычислениях: %s', self.result_error.text_error),
            call('Статус не определен: %s', self.result_unknown_status.status)
        ]
        self_mock.logger.warning.assert_has_calls(calls_warning, any_order=False)


if __name__ == '__main__':
    main()
