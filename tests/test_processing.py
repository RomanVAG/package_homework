import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_transactions():
    """Фикстура, возвращающая тестовый список транзакций для использования в тестах.

    Returns:
        list[dict]: Список словарей, каждый из которых представляет транзакцию с полями:
            - id (int): Уникальный идентификатор транзакции.
            - state (str): Статус транзакции ("EXECUTED" или "CANCELED").
            - date (str): Дата и время транзакции в формате ISO.
    """
    return [
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364"
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689"
        },
        {
            "id": 615064591,
            "state": "CANCELED",
            "date": "2018-10-14T08:21:33.419441"
        },
    ]


@pytest.fixture
def corrupted_transactions():
    """Фикстура с транзакциями, содержащими некорректные данные."""
    return [
        {"id": 1, "state": "EXECUTED"},  # Нет даты
        {"id": 2, "date": "2019-07-03T18:35:29.512364"},  # Нет статуса
        {"id": 3},  # Только id
    ]


# Тесты для filter_by_state
def test_filter_by_state_executed(sample_transactions):
    filtered = filter_by_state(sample_transactions, "EXECUTED")
    assert len(filtered) == 2
    assert all(t["state"] == "EXECUTED" for t in filtered)


def test_filter_by_state_canceled(sample_transactions):
    filtered = filter_by_state(sample_transactions, "CANCELED")
    assert len(filtered) == 2
    assert all(t["state"] == "CANCELED" for t in filtered)


def test_filter_by_state_default(sample_transactions):
    filtered = filter_by_state(sample_transactions)
    assert len(filtered) == 2
    assert all(t["state"] == "EXECUTED" for t in filtered)


def test_filter_by_state_empty(sample_transactions):
    filtered = filter_by_state(sample_transactions, "PENDING")
    assert len(filtered) == 0


def test_filter_empty_list():
    """Тестирует фильтрацию пустого списка транзакций."""
    assert len(filter_by_state([], "EXECUTED")) == 0


def test_filter_corrupted_data(corrupted_transactions):
    """Тестирует фильтрацию списка с некорректными данными."""
    filtered = filter_by_state(corrupted_transactions, "EXECUTED")
    assert len(filtered) == 1
    assert filtered[0]["id"] == 1


# Тесты для sort_by_date
def test_sort_by_date_descending(sample_transactions):
    sorted_transactions = sort_by_date(sample_transactions)
    dates = [t["date"] for t in sorted_transactions]
    assert dates == [
        "2019-07-03T18:35:29.512364",
        "2018-10-14T08:21:33.419441",
        "2018-09-12T21:27:25.241689",
        "2018-06-30T02:08:58.425572",
    ]


def test_sort_by_date_ascending(sample_transactions):
    sorted_transactions = sort_by_date(sample_transactions, False)
    dates = [t["date"] for t in sorted_transactions]
    assert dates == [
        "2018-06-30T02:08:58.425572",
        "2018-09-12T21:27:25.241689",
        "2018-10-14T08:21:33.419441",
        "2019-07-03T18:35:29.512364",
    ]


def test_sort_empty_list():
    """Тестирует сортировку пустого списка транзакций."""
    assert len(sort_by_date([])) == 0


def test_sort_single_transaction():
    """Тестирует сортировку списка с одной транзакцией."""
    single = [{"id": 1, "date": "2019-01-01T00:00:00.000000"}]
    result = sort_by_date(single)
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_sort_corrupted_data(corrupted_transactions):
    """Тестирует сортировку списка с некорректными данными."""
    with pytest.raises(KeyError):
        sort_by_date(corrupted_transactions)


def test_sort_missing_date_field():
    """Тестирует обработку транзакции без поля даты."""
    transactions = [{"id": 1, "state": "EXECUTED"}]
    with pytest.raises(KeyError):
        sort_by_date(transactions)
