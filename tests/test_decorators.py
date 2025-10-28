import pytest

from unittest.mock import patch
from datetime import datetime

from src.decorators import log, my_function


class Testlog:
    """Тесты для декоратора log"""

    @patch('src.decorators.datetime')
    def test_log_console(self, mock_now, capsys):
        # self = этот тест (объект Testlog)
        # mock_now = замоканный datetime
        # capsys = для перехвата вывода
        """
        Тестирование вывода в консоль, если файл mylog.txt не задан
        """
        # Фиксируем конкретное время
        fixed_time = datetime(2025, 10, 28, 12, 00, 0)
        mock_now.now.return_value = fixed_time
        decorated_function = log()(my_function)
        result = decorated_function(7, 6)
        captured = capsys.readouterr()
        expected = f"{fixed_time.strftime('%Y/%m/%d, %H:%M:%S')} my_function ok: {result}"
        assert expected in captured.out

    # def test_log_file(lecapsys):
    #     """
    #     Тестирование вывода в файл, если файл mylog.txt задан
    #     """
    #     @log()
    #     my_function()
    #     captured = capsys.readouterr()
    #     assert captured.out == "2024-01-15 14:30:25 k- my_function ok"

    # def test_log_console_Exception(capsys):
    #     """
    #     Тестирование вывода в консоль исключения типа Exception, если файл mylog.txt не задан
    #     """
    #     @log()
    #     my_function()
    #     captured = capsys.readouterr()
    #     assert captured.out == "2024-01-15 14:30:25 k- my_function ok"
    #
    #
    # def test_log_file_Exception(capsys):
    #     """
    #     Тестирование вывода в консоль исключения типа Exception, если файл mylog.txt не задан
    #     """
    #     @log()
    #     my_function()
    #     captured = capsys.readouterr()
    #     assert captured.out == "2024-01-15 14:30:25 k- my_function ok"
