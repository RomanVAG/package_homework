import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "input_str, expected",
    [
        # Базовые случаи
        ("", ""),
        ("   ", "   "),
        ("Счет", "Счет"),
        ("Карта", "Карта"),
        # Тесты для счетов (разные форматы и регистры)
        ("Счет 12345678901234567890", "Счет **7890"),
        ("сЧет 12345678901234567890", "сЧет **7890"),
        ("СЧЕТ 12345678901234567890", "СЧЕТ **7890"),
        # Тесты для карт (разные платежные системы)
        ("Карта 1234567812345678", "Карта 1234 56** **** 5678"),
        ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
        ("Visa Platinum 1234567812345678", "Visa Platinum 1234 56** **** 5678"),
        ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
        ("МИР 1234567812345678", "МИР 1234 56** **** 5678"),
        ("JCB 1234567812345678", "JCB 1234 56** **** 5678"),
        # Тесты с пробелами
        ("  Счет  12345678901234567890  ", "Счет **7890"),
        ("  Visa  1234567812345678  ", "Visa 1234 56** **** 5678"),
        ("  Карта  1234567812345678  ", "Карта 1234 56** **** 5678"),
        ("Карта  1234567812345678", "Карта 1234 56** **** 5678"),  # Двойной пробел
        ("Счет\t12345678901234567890", "Счет **7890"),  # Табуляция вместо пробела
        ("Карта 1234 5678 9012 3456", "Карта 1234 56** **** 3456"),
        ("Visa 1234 5678 9012 3456", "Visa 1234 56** **** 3456"),
        # Комбинированные случаи
        ("Счет корпоративный 12345678901234567890", "Счет корпоративный **7890"),
        ("Карта зарплатная 1234567812345678", "Карта зарплатная 1234 56** **** 5678"),
        ("Доп. карта 1234567812345678", "Доп. карта 1234 56** **** 5678"),
        # Граничные случаи
        ("Счет 00000000000000000001", "Счет **0001"),
        ("Карта 0000111122223333", "Карта 0000 11** **** 3333"),
        ("Карта 0000000000000000", "Карта 0000 00** **** 0000"),
    ],
)
def test_mask_account_card(input_str: str, expected: str) -> None:
    """Проверяет корректность маскировки для различных типов карт и счетов."""
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize(
    "input_str, expected_exception, error_msg",
    [
        # Некорректные символы в номере
        ("Счет 548abcdef", ValueError, "Номер счета должен содержать только цифры"),
        ("Карта 1234abcd5678efgh", ValueError, "Номер карты должен содержать только цифры"),
        # Некорректные типы данных
        (1234567812345678, ValueError, "Входные данные должны быть строкой"),
        (None, ValueError, "Входные данные должны быть строкой"),
        # Слишком длинные номера счетов
        ("Счет 123456789012345678901", ValueError, "Номер счета должен содержать 20 цифр"),
        # Нестандартная длина счетов
        ("Счет 1234567890123456", ValueError, "Номер счета должен содержать 20 цифр"),
        ("Счет 1234", ValueError, "Номер счета должен содержать 20 цифр"),
        # Неполные/некорректные номера карт
        ("Карта 1234", ValueError, "Номер карты должен содержать 16 цифр"),
        ("Visa 12345678", ValueError, "Номер карты должен содержать 16 цифр"),
        ("Карта 123456781234", ValueError, "Номер карты должен содержать 16 цифр"),
        # Слишком длинные номера карт
        ("Карта 12345678123456781234", ValueError, "Номер карты должен содержать 16 цифр"),
        ("Visa 123456781234567812345", ValueError, "Номер карты должен содержать 16 цифр"),
        ("MasterCard 12345678123456789", ValueError, "Номер карты должен содержать 16 цифр"),
        # Граничные случаи длины
        ("Карта 123456781234567", ValueError, "Номер карты должен содержать 16 цифр"),
        ("Карта 12345678123456781", ValueError, "Номер карты должен содержать 16 цифр"),
    ],
)
def test_mask_account_card_errors(
    input_str: str | int | None, expected_exception: type[Exception], error_msg: str
) -> None:
    """Проверяет обработку некорректных входных данных."""
    with pytest.raises(expected_exception) as excinfo:
        mask_account_card(input_str)  # type: ignore[arg-type]
    assert error_msg in str(excinfo.value)


@pytest.mark.parametrize(
    "input_date,expected",
    [
        ("2023-12-31T23:59:59.999", "31.12.2023"),
        ("2020-02-29T00:00:00.000", "29.02.2020"),
        ("1999-01-01T00:00:00", "01.01.1999"),
        ("2050-06-15T12:30:45", "15.06.2050"),
        ("0001-01-01T00:00:00", "01.01.0001"),
    ],
    ids=[
        "normal_case",
        "leap_year",
        "millenium_change",
        "future_date",
        "min_date",
    ],
)
def test_valid_date_formats(input_date: str, expected: str) -> None:
    """Тестирование корректных форматов даты."""
    result = get_date(input_date)
    assert result == expected, f"Ожидалось {expected}, получено {result}"
    assert len(result) == 10
    assert result[2] == "." and result[5] == "."
    day, month, year = result.split(".")
    assert day.isdigit() and len(day) == 2 and 1 <= int(day) <= 31
    assert month.isdigit() and len(month) == 2 and 1 <= int(month) <= 12
    assert year.isdigit() and len(year) == 4


@pytest.mark.parametrize(
    "invalid_input,expected_exception,error_pattern",
    [
        ("2023-12-31 23:59:59", ValueError, "Отсутствует разделитель 'T'"),
        ("2023-12-31", ValueError, "Отсутствует разделитель 'T'"),
        ("31.12.2023", ValueError, "Неверный формат даты"),
        ("2023/12/31T00:00:00", ValueError, "Неверный формат даты"),
        ("2023-13-01T00:00:00", ValueError, "Недопустимый месяц"),
        ("2023-02-30T00:00:00", ValueError, "Недопустимый день"),
        ("2023-04-31T00:00:00", ValueError, "Недопустимый день"),
        ("", IndexError, "Пустая строка даты"),
        ("Just a string", ValueError, "Неверный формат даты"),
        ("Transaction: 2023-12-31T...", ValueError, "Неверный формат даты"),
    ],
    ids=[
        "space_separator",
        "date_only",
        "reverse_format",
        "slash_separator",
        "invalid_month",
        "invalid_day_feb",
        "invalid_day_apr",
        "empty_string",
        "random_text",
        "prefix_text",
    ],
)
def test_invalid_inputs(invalid_input: str, expected_exception: type[Exception], error_pattern: str) -> None:
    """Проверка обработки некорректных входных данных."""
    with pytest.raises(expected_exception) as exc_info:
        get_date(invalid_input)
    assert error_pattern in str(exc_info.value)


def test_return_type_and_format() -> None:
    """Комплексная проверка типа возвращаемого значения и его формата."""
    test_date = "2023-12-31T23:59:59.999"
    result = get_date(test_date)

    assert isinstance(result, str)
    parts = result.split(".")
    assert len(parts) == 3

    day, month, year = parts
    assert len(day) == 2 and day.isdigit() and 1 <= int(day) <= 31
    assert len(month) == 2 and month.isdigit() and 1 <= int(month) <= 12
    assert len(year) == 4 and year.isdigit() and int(year) > 0


@pytest.mark.parametrize(
    "input_date,expected",
    [
        ("2023-01-01T00:00:00", "01.01.2023"),
        pytest.param(
            "2023-1-1T00:00:00",
            None,
            marks=pytest.mark.xfail(
                raises=ValueError, reason="Функция требует обязательного использования ведущих нулей"
            ),
        ),
    ],
    ids=[
        "with_leading_zeros",
        "without_leading_zeros",
    ],
)
def test_leading_zeros_handling(input_date: str, expected: str | None) -> None:
    """Проверка обязательного использования ведущих нулей."""
    if expected is None:
        with pytest.raises(ValueError):
            get_date(input_date)
    else:
        assert get_date(input_date) == expected
