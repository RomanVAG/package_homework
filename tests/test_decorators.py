import os
from datetime import datetime
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from src.decorators import log, my_function


@pytest.fixture
def manage_log_file() -> Generator[None, None, None]:
    """
    Фикстура для управления временным файлом лога 'mylog.txt'.

    Действия:
    - Перед тестом: удаляет файл, если он существует.
    - После теста: удаляет файл, если он был создан.

    Yields:
        None (используется для разделения кода до и после теста).
    """
    # Удаление файла перед тестом
    if os.path.exists("mylog.txt"):
        os.remove("mylog.txt")
    yield  # Точка разделения: код до yield — до теста, после — после теста
    # Удаление файла после теста
    if os.path.exists("mylog.txt"):
        os.remove("mylog.txt")


@pytest.mark.usefixtures("manage_log_file")
class Testlog:
    """
    Набор тестов для проверки декоратора `log`.

    Проверяет:
    - Вывод в консоль при отсутствии файла лога.
    - Вывод ошибок в консоль.
    - Запись в файл при указании `filename`.
    - Запись ошибок в файл.
    """

    @patch("src.decorators.datetime")
    def test_log_console(self, mock_now: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """
        Тест: вывод успешного выполнения функции в консоль (без файла лога).

        Шаги:
        1. Замокаем `datetime.now()` для фиксированного времени.
        2. Применяем декоратор `log` к `my_function`.
        3. Вызываем функцию и перехватываем вывод в консоль.
        4. Проверяем, что вывод соответствует ожидаемому формату.

        Args:
            mock_now: замоканный объект `datetime` для контроля времени.
            capsys: фикстура pytest для перехвата stdout/stderr.
        """
        fixed_time = datetime(2025, 10, 28, 12, 00, 0)
        mock_now.now.return_value = fixed_time

        decorated_function = log()(my_function)
        result = decorated_function(7, 6)

        captured = capsys.readouterr()  # Фикстура, которая ловит вывод ошибки в консоль
        expected = f"{fixed_time.strftime('%Y/%m/%d, %H:%M:%S')} {my_function.__name__} ok: {result}"
        assert expected in captured.out

    @patch("src.decorators.datetime")
    def test_log_console_exception(self, mock_now: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """
        Тест: вывод ошибки в консоль (без файла лога).

        Проверяет, что при исключении:
        - В консоль записывается сообщение с ошибкой.
        - Формат соответствует ожиданиям.

        Args:
            mock_now: замоканный объект `datetime`.
            capsys: фикстура для перехвата вывода.
        """
        fixed_time = datetime(2025, 10, 28, 12, 00, 0)
        mock_now.now.return_value = fixed_time

        decorated_function = log()(my_function)

        with pytest.raises(TypeError):
            decorated_function("x", 6)

        captured = capsys.readouterr()  # Фикстура, которая ловит вывод ошибки в консоль
        expected = f"{fixed_time.strftime('%Y/%m/%d, %H:%M:%S')} "
        f"{my_function.__name__} error: {TypeError.__name__}. Inputs: ('x', 6), {{}}"
        assert expected in captured.out

    @patch("src.decorators.datetime")
    def test_log_file(self, mock_now: MagicMock) -> None:
        """
        Тест: запись успешного выполнения в файл 'mylog.txt'.

        Проверяет:
        - Создание файла лога.
        - Запись сообщения с фиксированным временем.
        - Соответствие формата ожидаемому.

        Args:
            mock_now: замоканный объект `datetime`.
        """

        fixed_time = datetime(2025, 10, 28, 12, 00, 0)
        mock_now.now.return_value = fixed_time

        decorated_function = log(filename="mylog.txt")(my_function)
        result = decorated_function(7, 6)

        with open("mylog.txt", "r", encoding="utf-8") as log_file:  # чтение информации из файла
            readline = log_file.read()

        expected = f"{fixed_time.strftime('%Y/%m/%d, %H:%M:%S')} {my_function.__name__} ok: {result}"
        assert expected in readline

    @patch("src.decorators.datetime")
    def test_log_file_exception(self, mock_now: MagicMock) -> None:
        """
        Тест: запись ошибки в файл 'mylog.txt'.

        Проверяет:
        - При исключении создаётся файл лога.
        - В файл записывается сообщение об ошибке.
        - Формат соответствует ожиданиям.

        Args:
            mock_now: замоканный объект `datetime`.
        """
        fixed_time = datetime(2025, 10, 28, 12, 00, 0)
        mock_now.now.return_value = fixed_time

        decorated_function = log(filename="mylog.txt")(my_function)

        with pytest.raises(TypeError):
            decorated_function("x", 6)

        with open("mylog.txt", "r", encoding="utf-8") as log_file:  # чтение информации из файла
            readline = log_file.read()

        expected = f"{fixed_time.strftime('%Y/%m/%d, %H:%M:%S')} "
        f"{my_function.__name__} error: {TypeError.__name__}. Inputs: ('x', 6), {{}}"
        assert expected in readline
