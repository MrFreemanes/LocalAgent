from unittest import TestCase, main
from unittest.mock import Mock, patch

from gui.main_window import MainWindow
from config.config import Task, Status, Result


class MainWindowTest(TestCase):
    """Тест класса MainWindow. Проверяет ключевые методы без запуска GUI."""

    # --- базовые методы UI ---
    @patch('gui.main_window.QProgressBar')
    @patch('gui.main_window.QLabel')
    @patch('gui.main_window.Ui_MainWindow')
    def test_setup_ui(self, ui_main_window_mock, label_mock, progress_mock):
        """Проверка корректной инициализации UI."""
        ui_mock = Mock()
        ui_main_window_mock.return_value = ui_mock

        self_mock = Mock()
        setup_ui = MainWindow._setup_ui

        setup_ui(self_mock)

        self.assertTrue(ui_main_window_mock.called)
        self.assertTrue(ui_mock.setupUi.called)
        self.assertEqual(self_mock.ui, ui_mock)
        self.assertEqual(self_mock.progress_bar.setValue.call_count, 1)
        self.assertEqual(self_mock.progress_bar.setValue.call_args[0][0], 0)

    def test_connect_bridge_signals(self):
        """Проверяет, что сигналы моста подключаются к _check_signal."""
        bridge_mock = Mock()
        bridge_mock.done_signal.connect = Mock()
        bridge_mock.process_signal.connect = Mock()

        self_mock = Mock()
        self_mock.bridge = bridge_mock

        MainWindow._connect_bridge_signals(self_mock)

        bridge_mock.done_signal.connect.assert_called_with(self_mock._check_signal)
        bridge_mock.process_signal.connect.assert_called_with(self_mock._check_signal)

    # --- вспомогательные кнопочные методы ---
    def test_off_all_btn(self):
        """Проверка отключения всех кнопок."""
        ui_mock = Mock()
        self_mock = Mock()
        self_mock.ui = ui_mock
        self_mock.logger = Mock()

        MainWindow._off_all_btn(self_mock)

        ui_mock.lineEdit_massage.setEnabled.assert_called_with(False)
        ui_mock.btn_init.setEnabled.assert_called_with(False)
        ui_mock.btn_massage.setEnabled.assert_called_with(False)
        self_mock.logger.debug.assert_called()

    def test_on_all_btn(self):
        """Проверка включения всех кнопок."""
        ui_mock = Mock()
        self_mock = Mock()
        self_mock.ui = ui_mock
        self_mock.logger = Mock()

        MainWindow._on_all_btn(self_mock)

        ui_mock.lineEdit_massage.setEnabled.assert_called_with(True)
        ui_mock.btn_init.setEnabled.assert_called_with(True)
        ui_mock.btn_massage.setEnabled.assert_called_with(True)
        self_mock.logger.debug.assert_called()

    # --- тестирование логики progress layout ---
    def test_create_and_clear_layout(self):
        """Проверяет добавление и очистку layout."""
        layout_mock = Mock()
        layout_mock.count.side_effect = [2, 0]  # будет 2 итерации
        item1 = Mock()
        item2 = Mock()
        layout_mock.takeAt.side_effect = [item1, item2]
        item1.widget.return_value = Mock()
        item2.widget.return_value = None
        item2.layout.return_value = Mock()

        self_mock = Mock()
        self_mock.ui = Mock()
        self_mock.ui.horizontalLayout_progress = layout_mock
        self_mock.progress_label = Mock()
        self_mock.progress_bar = Mock()
        self_mock.logger = Mock()

        # create layout
        MainWindow._create_layout_progress(self_mock)
        self_mock.ui.horizontalLayout_progress.addWidget.assert_any_call(self_mock.progress_label)
        self_mock.ui.horizontalLayout_progress.addWidget.assert_any_call(self_mock.progress_bar)

        # clear layout
        MainWindow._clear_layout(self_mock, layout_mock)
        self_mock.logger.debug.assert_called()

    # --- тесты на _check_signal ---
    def test_check_signal_scanning_done(self):
        """Проверяет реакцию при завершении сканирования."""
        result = Result(status=Status.DONE,
                        data={'worker': 'scanning'},
                        progress=100)
        self_mock = Mock()
        self_mock.progress_label = Mock()
        self_mock.progress_bar = Mock()
        self_mock.logger = Mock()

        MainWindow._check_signal(self_mock, result)
        self_mock.progress_label.setText.assert_called_with('Сканирование завершено.')
        self_mock.progress_bar.setValue.assert_called_with(100)

    def test_check_signal_vector_done(self):
        """Проверяет реакцию при завершении векторизации."""
        result = Result(status=Status.DONE,
                        data={'worker': 'vector'},
                        progress=100)
        self_mock = Mock()
        self_mock.progress_bar = Mock()
        self_mock.logger = Mock()
        self_mock._clear_layout = Mock()
        self_mock._on_all_btn = Mock()
        self_mock.ui = Mock()
        self_mock.ui.horizontalLayout_progress = Mock()

        MainWindow._check_signal(self_mock, result)
        self_mock._clear_layout.assert_called_with(self_mock.ui.horizontalLayout_progress)
        self_mock._on_all_btn.assert_called()
        self_mock.logger.debug.assert_called()

    def test_check_signal_request_done(self):
        """Проверяет реакцию при завершении запроса."""
        result = Result(data={'worker': 'request', 'data': []},
                        status=Status.DONE,
                        progress=100)
        self_mock = Mock()
        self_mock._check_result = Mock()
        self_mock.logger = Mock()

        MainWindow._check_signal(self_mock, result)
        self_mock._check_result.assert_called_with(result)
        self_mock.logger.debug.assert_called()

    # --- тест _send_request ---
    def test_send_request_empty(self):
        """Не должен отправлять, если строка пуста."""
        ui_mock = Mock()
        ui_mock.lineEdit_massage.text.return_value = "   "
        self_mock = Mock()
        self_mock.ui = ui_mock

        MainWindow._send_request(self_mock)
        self.assertFalse(self_mock.bridge.send_task.called)

    def test_send_request_success(self):
        """Проверяет корректное создание задачи и очистку поля."""
        ui_mock = Mock()
        ui_mock.lineEdit_massage.text.return_value = "привет"
        ui_mock.textEdit_chat.append = Mock()
        ui_mock.lineEdit_massage.clear = Mock()

        self_mock = Mock()
        self_mock.ui = ui_mock
        self_mock.bridge = Mock()
        self_mock.logger = Mock()

        MainWindow._send_request(self_mock)

        self_mock.bridge.send_task.assert_called()
        ui_mock.textEdit_chat.append.assert_any_call("<b>Запрос:</b> привет")
        ui_mock.lineEdit_massage.clear.assert_called()
        self_mock.logger.debug.assert_called()

    # --- тест _check_result ---
    def test_check_result_no_data(self):
        """Если данных нет — ничего не добавляется."""
        result = Result(status=Status.DONE,
                        data={'data': []},
                        progress=100)
        ui_mock = Mock()
        self_mock = Mock()
        self_mock.ui = ui_mock

        MainWindow._check_result(self_mock, result)
        self.assertFalse(ui_mock.textEdit_chat.append.called)

    def test_check_result_with_data(self):
        """Проверка добавления ответа от модели."""
        data = [{'file_path': 'f.txt', 'chunk_index': 1, 'score': 0.99, 'text': 'abc' * 50}]
        result = Result(status=Status.DONE,
                        data={'data': data},
                        progress=100)
        ui_mock = Mock()
        ui_mock.textEdit_chat.append = Mock()
        self_mock = Mock()
        self_mock.ui = ui_mock
        self_mock.logger = Mock()
        self_mock._on_all_btn = Mock()

        MainWindow._check_result(self_mock, result)
        ui_mock.textEdit_chat.append.assert_any_call("<b>Ответ:</b>")
        self_mock._on_all_btn.assert_called()
        self_mock.logger.debug.assert_called()


if __name__ == '__main__':
    main()
