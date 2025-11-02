import pytest
import os

from unittest.mock import patch
from datetime import datetime

from src.decorators import log, my_function


@pytest.fixture
def manage_log_file():
    """фикстура, которая будет открывать файл перед тестом и удалять его после:"""
    # Код перед тестом (создание или очистка файла)
    if os.path.exists("mylog.txt"):
        os.remove("mylog.txt")
    yield
    # Код после теста (удаление файла)
    if os.path.exists("mylog.txt"):
        os.remove("mylog.txt")


class Testlog:
    """Тесты для декоратора log"""

    @patch('src.decorators.datetime')
    def test_log_console(self, mock_now, capsys, manage_log_file):
        # self = этот тест (объект Testlog)
        # mock_now = замоканный datetime
        # capsys = для перехвата вывода
        """
        Тестирование вывода my_function ok в консоль, если файл mylog.txt не задан
        """
        # Фиксируем конкретное время
        fixed_time = datetime(2025, 10, 28, 12, 00, 0)
        mock_now.now.return_value = fixed_time
        decorated_function = log()(my_function)
        result = decorated_function(7, 6)
        captured = capsys.readouterr()  # Фикстура, которая ловит вывод ошибки в консоль
        expected = f"{fixed_time.strftime('%Y/%m/%d, %H:%M:%S')} {my_function.__name__} ok: {result}"
        assert expected in captured.out

    @patch('src.decorators.datetime')
    def test_log_console_Exception(self, mock_now, capsys, manage_log_file):
        # self = этот тест (объект Testlog)
        # mock_now = замоканный datetime
        # capsys = для перехвата вывода
        """
        Тестирование вывода в консоль исключения типа Exception, если файл mylog.txt не задан
        """
        # Фиксируем конкретное время
        fixed_time = datetime(2025, 10, 28, 12, 00, 0)
        mock_now.now.return_value = fixed_time
        decorated_function = log()(my_function)
        with pytest.raises(TypeError):
            decorated_function("x", 6)
        captured = capsys.readouterr()  # Фикстура, которая ловит вывод ошибки в консоль
        expected = f"{fixed_time.strftime('%Y/%m/%d, %H:%M:%S')} {my_function.__name__} error: {TypeError.__name__}. Inputs: ('x', 6), {{}}"
        assert expected in captured.out

    @patch('src.decorators.datetime')
    def test_log_file(self, mock_now, manage_log_file):
        # self = этот тест (объект Testlog)
        # mock_now = замоканный datetime
        """
        Тестирование вывода my_function ok в файл, если файл mylog.txt задан
        """
        # Фиксируем конкретное время
        fixed_time = datetime(2025, 10, 28, 12, 00, 0)
        mock_now.now.return_value = fixed_time
        decorated_function = log(filename="mylog.txt")(my_function)
        result = decorated_function(7, 6)
        with open("mylog.txt", "r", encoding='utf-8') as _:  # чтение информации из файла
            readline = _.read()
        expected = f"{fixed_time.strftime('%Y/%m/%d, %H:%M:%S')} {my_function.__name__} ok: {result}"
        assert expected in readline

    @patch('src.decorators.datetime')
    def test_log_file_Exception(self, mock_now, manage_log_file):
        # self = этот тест (объект Testlog)
        # mock_now = замоканный datetime
        """
        Тестирование вывода в файл исключения типа Exception, если файл mylog.txt задан
        """
        # Фиксируем конкретное время
        fixed_time = datetime(2025, 10, 28, 12, 00, 0)
        mock_now.now.return_value = fixed_time
        decorated_function = log(filename="mylog.txt")(my_function)
        with pytest.raises(TypeError):
            decorated_function("x", 6)
        with open("mylog.txt", "r", encoding='utf-8') as _:  # чтение информации из файла
            readline = _.read()
        expected = f"{fixed_time.strftime('%Y/%m/%d, %H:%M:%S')} {my_function.__name__} error: {TypeError.__name__}. Inputs: ('x', 6), {{}}"
        assert expected in readline
