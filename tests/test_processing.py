import pytest

from src.processing import filter_by_state, sort_by_date

@pytest.fixture
def sample_operations():
    return [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "CANCELED", "amount": 200},
        {"id": 3, "state": "EXECUTED", "amount": 300},
        {"id": 4, "state": "PENDING", "amount": 400},
        {"id": 5, "state": "EXECUTED", "amount": 500},
    ]


def test_filter_by_state_default(sample_operations):
    """Тестирование фильтрации по умолчанию (state=EXECUTED)."""
    result = filter_by_state(sample_operations)
    expected = [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 3, "state": "EXECUTED", "amount": 300},
        {"id": 5, "state": "EXECUTED", "amount": 500},
    ]
    assert result == expected


def test_filter_by_state_canceled(sample_operations):
    """Тестирование фильтрации по state=CANCELED."""
    result = filter_by_state(sample_operations, "CANCELED")
    expected = [{"id": 2, "state": "CANCELED", "amount": 200}]
    assert result == expected


def test_filter_by_state_pending(sample_operations):
    """Тестирование фильтрации по state=PENDING."""
    result = filter_by_state(sample_operations, "PENDING")
    expected = [{"id": 4, "state": "PENDING", "amount": 400}]
    assert result == expected


def test_filter_by_state_empty_result():
    """Тестирование случая, когда нет операций с указанным state."""
    operations = [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "EXECUTED", "amount": 200},
    ]
    result = filter_by_state(operations, "CANCELED")
    assert result == []


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3, 5]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state_parametrized(sample_operations, state, expected_ids):
    """Параметризованный тест для различных значений state."""
    result = filter_by_state(sample_operations, state)
    assert [op["id"] for op in result] == expected_ids


def test_filter_by_state_empty_input():
    """Тестирование функции с пустым списком операций."""
    result = filter_by_state([], "EXECUTED")
    assert result == []


# @pytest.fixture
# def sample_transactions():
#     return [
#         {"id": 1, "date": "2023-01-15T12:00:00"},
#         {"id": 2, "date": "2022-05-20T08:30:00"},
#         {"id": 3, "date": "2023-03-10T15:45:00"},
#         {"id": 4, "date": "2021-12-31T23:59:59"},
#     ]
#
#
# def test_sort_by_date_default(sample_transactions):
#     """Тестирование сортировки по умолчанию (reverse=True, новые → старые)."""
#     result = sort_by_date(sample_transactions)
#     expected_dates = [
#         "2023-03-10T15:45:00",
#         "2023-01-15T12:00:00",
#         "2022-05-20T08:30:00",
#         "2021-12-31T23:59:59",
#     ]
#     assert [tx["date"] for tx in result] == expected_dates
#
#
# def test_sort_by_date_ascending(sample_transactions):
#     """Тестирование сортировки по возрастанию даты (reverse=False)."""
#     result = sort_by_date(sample_transactions, reverse=False)
#     expected_dates = [
#         "2021-12-31T23:59:59",
#         "2022-05-20T08:30:00",
#         "2023-01-15T12:00:00",
#         "2023-03-10T15:45:00",
#     ]
#     assert [tx["date"] for tx in result] == expected_dates
#
#
# def test_sort_by_date_empty_list():
#     """Тестирование сортировки пустого списка."""
#     assert sort_by_date([]) == []
#     assert sort_by_date([], reverse=False) == []
#
#
# def test_sort_by_date_single_element():
#     """Тестирование сортировки списка с одной транзакцией."""
#     single_tx = [{"id": 1, "date": "2023-01-01T00:00:00"}]
#     assert sort_by_date(single_tx) == single_tx
#     assert sort_by_date(single_tx, reverse=False) == single_tx
#
#
# @pytest.mark.parametrize(
#     "reverse, expected_ids",
#     [
#         (True, [3, 1, 2, 4]),  # новые → старые
#         (False, [4, 2, 1, 3]), # старые → новые
#     ],
# )
# def test_sort_by_date_parametrized(sample_transactions, reverse, expected_ids):
#     """Параметризованный тест для разных направлений сортировки."""
#     result = sort_by_date(sample_transactions, reverse=reverse)
#     assert [tx["id"] for tx in result] == expected_ids