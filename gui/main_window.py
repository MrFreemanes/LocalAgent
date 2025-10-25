from PySide6.QtWidgets import QFileDialog, QLabel, QProgressBar

from gui.base_window import BaseWindow
from gui.ui.ui_untitled import Ui_MainWindow
from config.config import Task, Status


class MainWindow(BaseWindow):
    def _setup_ui(self) -> None:
        """Обозначение главных переменных."""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Test')

        self.ui.lineEdit_massage.setPlaceholderText("Введите запрос, например: 'веселые стрекозы'")

        self.path_to_dir = None
        self.progress_label = QLabel()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

    def _connect_widget(self) -> None:
        """Подключение виджетов к функциям."""
        self.ui.btn_init.clicked.connect(self._run_init)
        self.ui.btn_massage.clicked.connect(self._send_message)
        self.ui.lineEdit_massage.returnPressed.connect(self._send_message)

    def _connect_bridge_signals(self) -> None:
        """Подключение сигналов из моста."""
        self.bridge.process_signal.connect(self._check_signal)
        self.bridge.done_signal.connect(self._check_signal)

    # --- реализация приложения ---
    def _run_init(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с заметками")
        if folder == '':
            return
        self.path_to_dir = folder
        self.ui.label_dir.setText(self.path_to_dir)

        self.bridge.send_task(Task('init', self.path_to_dir))

        self._create_layout_progress()
        self._run_scan()
        self._run_vector()

    def _run_scan(self):
        self._off_all_btn()
        self.bridge.send_task(Task('scanning', self.path_to_dir))
        self.progress_label.setText('Сканирование... Пожалуйста подождите.')

    def _run_vector(self):
        self._off_all_btn()
        self.bridge.send_task(Task('vector', self.path_to_dir))
        self.progress_label.setText('Векторизация... Это займет время.')

    def _check_signal(self, result):
        worker = result.data['worker']
        if worker == 'scanning':
            if result.status == Status.RUN:
                self.progress_bar.setValue(result.progress)
            elif result.status == Status.DONE:
                self.progress_label.setText('Сканирование завершено.')
                self.progress_bar.setValue(result.progress)
        elif worker == 'vector':
            if result.status == Status.RUN:
                self.progress_bar.setValue(result.progress)
            elif result.status == Status.DONE:
                self._clear_layout(self.ui.horizontalLayout_progress)
                self._on_all_btn()

    def _off_all_btn(self):
        self.ui.btn_init.setEnabled(False)
        self.ui.btn_massage.setEnabled(False)

    def _on_all_btn(self):
        self.ui.btn_init.setEnabled(True)
        self.ui.btn_massage.setEnabled(True)

    def _create_layout_progress(self):
        self.ui.horizontalLayout_progress.addWidget(self.progress_label)
        self.ui.horizontalLayout_progress.addWidget(self.progress_bar)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if sub_layout is not None:
                    self._clear_layout(sub_layout)

    def _send_message(self):
        text = self.ui.lineEdit_massage.text().strip()
        if not text:
            return

        self.ui.textEdit_chat.append(f"<b>Запрос:</b> {text}")
        self.ui.lineEdit_massage.clear()
