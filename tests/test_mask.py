import pytest

from src.mask import get_mask_card_number, get_mask_account


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        (1234567890123456, "1234 56** **** 3456"),
    ],
)
def test_valid_card_numbers(card_number, expected):
    """Проверяет корректную маскировку валидных номеров карт"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "card_number, error_msg",
    [
        # Неправильная длина
        ("1234567890", "Номер карты должен содержать 16 цифр"),
        ("12345678901234567890", "Номер карты должен содержать 16 цифр"),
        ("", "Номер карты должен содержать 16 цифр"),
        # Недопустимые символы
        ("1234abcd56789012", "Номер карты должен содержать только цифры"),
        ("1234!@#$56789012", "Номер карты должен содержать только цифры"),
        # Недопустимый тип
        (None, "Номер карты должен быть строкой или числом"),
        (True, "Номер карты должен быть строкой или числом"),
        (12.34, "Номер карты должен быть строкой или числом"),
    ],
)
def test_invalid_card_numbers(card_number, error_msg):
    """Проверяет обработку некорректных номеров карт"""
    with pytest.raises(ValueError, match=error_msg):
        get_mask_card_number(card_number)


@pytest.mark.parametrize(
    "account, expected",
    [
        ("12345678901234567890", "**7890"),
        (12345678901234567890, "**7890"),
        ("00000000000000000001", "**0001"),
    ],
    ids=[
        "20 цифр строка",
        "20 цифр число",
        "20 цифр строка",
    ],
)
def test_valid_accounts(account, expected):
    """Тестирование корректных номеров счетов"""
    assert get_mask_account(account) == expected


@pytest.mark.parametrize(
    "account, error_msg",
    [
        ("", "Номер счета не может быть пустым"),
        ("abcd", "Номер счета должен содержать только цифры"),
        ("1234abcd", "Номер счета должен содержать только цифры"),
        ("1234!@#$", "Номер счета должен содержать только цифры"),
        ("!@#$%^", "Номер счета должен содержать только цифры"),
        (None, "Номер счета не может быть None"),
        (True, "Номер счета должен быть строкой или числом"),
        (False, "Номер счета должен быть строкой или числом"),
    ],
    ids=[
        "пустая строка",
        "только буквы",
        "цифры и буквы",
        "цифры и спецсимволы",
        "только спецсимволы",
        "None",
        "True",
        "False",
    ],
)
def test_invalid_accounts(account, error_msg):
    """Тестирование некорректных входных данных"""
    with pytest.raises(ValueError, match=error_msg):
        get_mask_account(account)
