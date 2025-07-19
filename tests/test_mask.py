import pytest

from src.mask import get_mask_card_number

@pytest.mark.parametrize("card_number, expected", [
    # Корректные данные
    ("1234567890123456", "1234 56** **** 3456"),
    (1234567890123456, "1234 56** **** 3456"),
])
def test_valid_card_numbers(card_number, expected):
    """Проверяет, что функция get_mask_card_number правильно маскирует номер карты"""
    assert get_mask_card_number(card_number) == expected

@pytest.mark.parametrize("card_number, error_msg", [
    # Неправильная длина
    ("1234567890", "Номер карты должен содержать 16 цифр"),
    ("12345678901234567890", "Номер карты должен содержать 16 цифр"),
    ("", "Номер карты должен содержать 16 цифр"),
    # Недопустимые символы
    ("1234abcd56789012", "Номер карты должен содержать только цифры"),
    ("1234!@#$56789012", "Номер карты должен содержать только цифры"),
    # Недопустимый тип
    (None, "Номер карты должен быть строкой или числом"),
])


def test_invalid_card_numbers(card_number, error_msg):
    """Проверяет, что функция get_mask_card_number корректно вызывает ValueError с соответствующими сообщениями"""
    with pytest.raises(ValueError, match=error_msg):
        get_mask_card_number(card_number)
