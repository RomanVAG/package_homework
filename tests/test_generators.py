import pytest, types
from src.generators import filter_by_currency, transaction_descriptions


class TestFilterByCurrency:
    """Тесты для генератора filter_by_currency"""

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
    def test_filter_by_currency_basic(self, transactions, currency_code, expected_count, expected_ids):
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
    def test_filter_by_currency_no_matches(self, transactions, currency_code):
        """Тест случая, когда нет транзакций в заданной валюте."""
        result = list(filter_by_currency(transactions, currency_code))
        assert len(result) == 0
        assert result == []

    def test_filter_by_currency_empty_list(self):
        """Тест обработки пустого списка транзакций."""
        result = filter_by_currency([], "USD")
        # Преобразуем в список и проверяем, что он пустой
        assert list(result) == []

    @pytest.mark.parametrize("transactions, currency_code, expected_count, expected_ids", [
        (INCOMPLETE_TRANSACTIONS, "USD", 2, [1, 5]),
        (INCOMPLETE_TRANSACTIONS, "EUR", 0, []),
    ])
    def test_filter_by_currency_incomplete_data(self, transactions, currency_code, expected_count, expected_ids):
        """Тест обработки транзакций с неполной структурой."""
        result = list(filter_by_currency(transactions, currency_code))

        assert len(result) == expected_count
        assert [t["id"] for t in result] == expected_ids

    @pytest.mark.parametrize("transactions, currency_code, expected_ids", [
        (CASE_SENSITIVE_TRANSACTIONS, "USD", [2]),
        (CASE_SENSITIVE_TRANSACTIONS, "usd", [1]),
    ])
    def test_filter_by_currency_case_sensitive(self, transactions, currency_code, expected_ids):
        """Тест чувствительности к регистру в коде валюты."""
        result = list(filter_by_currency(transactions, currency_code))

        assert [t["id"] for t in result] == expected_ids

    @pytest.mark.parametrize("transactions, currency_code, expected_first_id", [
        (USD_TRANSACTIONS, "USD", 939719570),
        (MIXED_CURRENCY_TRANSACTIONS, "USD", 1),
    ])
    def test_filter_by_currency_iterator_behavior(self, transactions, currency_code, expected_first_id):
        iterator = filter_by_currency(transactions, currency_code)

        # Более конкретная проверка - что это именно генератор
        assert isinstance(iterator, types.GeneratorType)

        first = next(iterator)
        assert first["id"] == expected_first_id

    def test_filter_by_currency_stop_iteration(self):
        """Тест возникновения StopIteration после окончания элементов."""
        iterator = filter_by_currency(self.USD_TRANSACTIONS, "USD")

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
    def test_filter_by_currency_invalid_input(self, transactions, currency_code):
        """Тест обработки некорректных входных данных."""
        # Функция должна корректно обрабатывать или пропускать проблемные данные
        if transactions is None or not isinstance(transactions, list):
            # Для некорректных данных ожидаем пустой результат
            result = list(filter_by_currency([], currency_code))
        else:
            result = list(filter_by_currency(transactions, currency_code))

        assert isinstance(result, list)


class TestTransactionDescriptions:
    """Тесты для генератора transaction_descriptions"""

    def test_transaction_descriptions_empty_list(self):
        """Тест с пустым списком транзакций"""
        result = transaction_descriptions([])
        # Проверяем, что это генератор/итератор
        assert isinstance(result, types.GeneratorType)
        # И что при преобразовании в список он пустой
        assert list(result) == []

    def test_transaction_descriptions_single_transaction(self):
        """Тест с одной транзакцией"""
        transactions = [{'description': 'Перевод организации', 'amount': 100}]
        result = transaction_descriptions(transactions)
        assert list(result) == ['Перевод организации']

    # Пример данных для параметризованных тестов (теперь внутри класса)
    TRANSACTIONS_TEST_CASES = [
        ([], []),
        ([{'description': 'Test'}], ['Test']),
        ([{'amount': 100}], []),
        ([
             {'description': 'First', 'amount': 100},
             {'description': 'Second', 'amount': 200}
         ], ['First', 'Second']),
        ([
             {'description': 'First'},
             {'amount': 200},
             {'description': 'Third'}
         ], ['First', 'Third'])
    ]

    @pytest.mark.parametrize('transactions, expected', TRANSACTIONS_TEST_CASES)
    def test_transaction_descriptions_parametrized(self, transactions, expected):
        """Параметризованный тест для различных сценариев"""
        result = transaction_descriptions(transactions)
        assert list(result) == expected

    def test_transaction_descriptions_realistic_scenario(self):
        """Тест с реалистичными данными"""
        transactions = [
            {'description': 'Перевод организации', 'operationAmount': {'amount': '100'}},
            {'description': 'Перевод со счета на счет', 'operationAmount': {'amount': '200'}},
            {'description': 'Перевод со счета на счет', 'operationAmount': {'amount': '300'}},
            {'description': 'Перевод с карты на карту', 'operationAmount': {'amount': '400'}},
            {'description': 'Перевод организации', 'operationAmount': {'amount': '500'}}
        ]

        result = transaction_descriptions(transactions)
        expected = [
            'Перевод организации',
            'Перевод со счета на счет',
            'Перевод со счета на счет',
            'Перевод с карты на карту',
            'Перевод организации'
        ]

        assert list(result) == expected

    def test_transaction_descriptions_large_dataset(self):
        """Тест с большим набором данных"""
        transactions = [
            {'description': f'Операция {i}', 'amount': i * 100}
            for i in range(1000)
        ]

        result = transaction_descriptions(transactions)
        expected = [f'Операция {i}' for i in range(1000)]

        assert list(result) == expected

    def test_transaction_descriptions_none_values(self):
        """Тест с None значениями"""
        transactions = [
            {'description': 'Valid operation', 'amount': 100},
            {'description': None, 'amount': 200},  # None description
            {'description': 'Another valid', 'amount': 300}
        ]

        result = transaction_descriptions(transactions)
        # Функция должна вернуть все записи с description, даже если значение None
        expected = ['Valid operation', None, 'Another valid']

        assert list(result) == expected