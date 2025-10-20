from multiprocessing.queues import Queue

from core.bridges.base_bridge import BaseBridge
from config.config import Status, Result


class Bridge(BaseBridge):
    """
    Реализация класса BaseBridge.
    """

    def __init__(self, task_q: Queue, result_q: Queue, *, interval: int = 100):
        super().__init__(task_q, result_q, interval)

    def _handle_result(self, result: Result) -> None:
        """Передача сигнала в зависимости от статуса результата."""
        stat = result.status
        if stat == Status.RUN:
            self.process_signal.emit(result)
            self.logger.debug('Получен промежуточный результат: %s', result.progress)
        elif stat == Status.DONE:
            self.done_signal.emit(result)
            self.logger.debug('Получен конечный результат: %s', result.__repr__())
        elif stat == Status.ERROR:
            self.error_signal.emit(f'Ошибка в вычислениях: {result.text_error}')
            self.logger.warning('Ошибка в вычислениях: %s', result.text_error)
        else:
            self.error_signal.emit(f'Статус не определен: {stat}')
            self.logger.warning('Статус не определен: %s', stat)
