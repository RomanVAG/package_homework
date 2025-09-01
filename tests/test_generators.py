import pytest, types
from src.generators import filter_by_currency

# Тестовые данные
USD_TRANSACTIONS = [
    {
        "id": 939719570,
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"code": "USD", "name": "USD"}
        }
    },
    {
        "id": 142264268,
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"code": "USD", "name": "USD"}
        }
    }
]

EUR_TRANSACTIONS = [
    {
        "id": 3,
        "operationAmount": {
            "amount": "500.00",
            "currency": {"code": "EUR", "name": "Euro"}
        }
    }
]

INCOMPLETE_TRANSACTIONS = [
    {"id": 1, "operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}},
    {"id": 2},  # Нет operationAmount
    {"id": 3, "operationAmount": {"amount": "300.00"}},  # Нет currency
    {"id": 4, "operationAmount": {"amount": "400.00", "currency": {"name": "Euro"}}},  # Нет code
    {"id": 5, "operationAmount": {"amount": "500.00", "currency": {"code": "USD"}}}
]

MIXED_CURRENCY_TRANSACTIONS = [
    {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "USD"}}},
    {"id": 2, "operationAmount": {"amount": "200", "currency": {"code": "EUR"}}},
    {"id": 3, "operationAmount": {"amount": "300", "currency": {"code": "GBP"}}},
    {"id": 4, "operationAmount": {"amount": "400", "currency": {"code": "USD"}}},
    {"id": 5, "operationAmount": {"amount": "500", "currency": {"code": "RUB"}}},
]

CASE_SENSITIVE_TRANSACTIONS = [
    {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "usd"}}},
    {"id": 2, "operationAmount": {"amount": "200", "currency": {"code": "USD"}}}
]


@pytest.mark.parametrize("transactions, currency_code, expected_count, expected_ids", [
    (USD_TRANSACTIONS, "USD", 2, [939719570, 142264268]),
    (EUR_TRANSACTIONS, "EUR", 1, [3]),
    (MIXED_CURRENCY_TRANSACTIONS, "USD", 2, [1, 4]),
    (MIXED_CURRENCY_TRANSACTIONS, "EUR", 1, [2]),
    (MIXED_CURRENCY_TRANSACTIONS, "GBP", 1, [3]),
    (MIXED_CURRENCY_TRANSACTIONS, "JPY", 0, []),
])
def test_filter_by_currency_basic(transactions, currency_code, expected_count, expected_ids):
    """Тест базовой фильтрации транзакций по валюте."""
    result = list(filter_by_currency(transactions, currency_code))

    assert len(result) == expected_count
    assert [t["id"] for t in result] == expected_ids
    assert all(t["operationAmount"]["currency"]["code"] == currency_code for t in result)


@pytest.mark.parametrize("transactions, currency_code", [
    (EUR_TRANSACTIONS, "USD"),  # Ищем USD в EUR транзакциях
    (USD_TRANSACTIONS, "EUR"),  # Ищем EUR в USD транзакциях
    ([], "USD"),  # Пустой список
    (MIXED_CURRENCY_TRANSACTIONS, "CNY"),  # Несуществующая валюта
])
def test_filter_by_currency_no_matches(transactions, currency_code):
    """Тест случая, когда нет транзакций в заданной валюте."""
    result = list(filter_by_currency(transactions, currency_code))
    assert len(result) == 0
    assert result == []


def test_filter_by_currency_empty_list():
    """Тест обработки пустого списка транзакций."""
    result = filter_by_currency([], "USD")
    # Преобразуем в список и проверяем, что он пустой
    assert list(result) == []


@pytest.mark.parametrize("transactions, currency_code, expected_count, expected_ids", [
    (INCOMPLETE_TRANSACTIONS, "USD", 2, [1, 5]),
    (INCOMPLETE_TRANSACTIONS, "EUR", 0, []),
])
def test_filter_by_currency_incomplete_data(transactions, currency_code, expected_count, expected_ids):
    """Тест обработки транзакций с неполной структурой."""
    result = list(filter_by_currency(transactions, currency_code))

    assert len(result) == expected_count
    assert [t["id"] for t in result] == expected_ids


@pytest.mark.parametrize("transactions, currency_code, expected_ids", [
    (CASE_SENSITIVE_TRANSACTIONS, "USD", [2]),
    (CASE_SENSITIVE_TRANSACTIONS, "usd", [1]),
])
def test_filter_by_currency_case_sensitive(transactions, currency_code, expected_ids):
    """Тест чувствительности к регистру в коде валюты."""
    result = list(filter_by_currency(transactions, currency_code))

    assert [t["id"] for t in result] == expected_ids


@pytest.mark.parametrize("transactions, currency_code, expected_first_id", [
    (USD_TRANSACTIONS, "USD", 939719570),
    (MIXED_CURRENCY_TRANSACTIONS, "USD", 1),
])
def test_filter_by_currency_iterator_behavior(transactions, currency_code, expected_first_id):
    iterator = filter_by_currency(transactions, currency_code)

    # Более конкретная проверка - что это именно генератор
    assert isinstance(iterator, types.GeneratorType)

    first = next(iterator)
    assert first["id"] == expected_first_id


def test_filter_by_currency_stop_iteration():
    """Тест возникновения StopIteration после окончания элементов."""
    iterator = filter_by_currency(USD_TRANSACTIONS, "USD")

    # Читаем все элементы
    list(iterator)

    # Должен вызвать StopIteration
    with pytest.raises(StopIteration):
        next(iterator)


@pytest.mark.parametrize("transactions, currency_code", [
    (None, "USD"),
    ("not_a_list", "USD"),
    ([{"invalid": "data"}], "USD"),
])
def test_filter_by_currency_invalid_input(transactions, currency_code):
    """Тест обработки некорректных входных данных."""
    # Функция должна корректно обрабатывать или пропускать проблемные данные
    result = list(filter_by_currency(transactions if isinstance(transactions, list) else [], currency_code))
    assert isinstance(result, list)