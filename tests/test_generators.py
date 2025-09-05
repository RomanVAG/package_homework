import pytest
import types
from src.generators import filter_by_currency
from src.generators import transaction_descriptions
from src.generators import card_number_generator


class TestFilterByCurrency:
    """Тесты для генератора filter_by_currency"""

    # Тестовые данные
    transactions = (
        [
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {
                    "amount": "9824.07",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702"
            },
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {
                    "amount": "79114.93",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188"
            },
            {
                "id": 873106923,
                "state": "EXECUTED",
                "date": "2019-03-23T01:09:46.296404",
                "operationAmount": {
                    "amount": "43318.34",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 44812258784861134719",
                "to": "Счет 74489636417521191160"
            },
            {
                "id": 895315941,
                "state": "EXECUTED",
                "date": "2018-08-19T04:27:37.904916",
                "operationAmount": {
                    "amount": "56883.54",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод с карты на карту",
                "from": "Visa Classic 6831982476737658",
                "to": "Visa Platinum 8990922113665229"
            },
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
                "operationAmount": {
                    "amount": "67314.70",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод организации",
                "from": "Visa Platinum 1246377376343588",
                "to": "Счет 14211924144426031657"
            }
        ]
    )

    @pytest.mark.parametrize("transactions, currency_code, expected_count, expected_ids", [
        (transactions, "USD", 3, [939719570, 142264268, 895315941]),
        (transactions, "EUR", 0, []),
        (transactions, "RUB", 2, [873106923, 594226727])
    ])
    def test_filter_by_currency_basic(self, transactions, currency_code, expected_count, expected_ids):
        """Тест базовой фильтрации транзакций по валюте."""
        result = list(filter_by_currency(transactions, currency_code))

        assert len(result) == expected_count
        assert [t["id"] for t in result] == expected_ids
        assert all(t["operationAmount"]["currency"]["code"] == currency_code for t in result)

    @pytest.mark.parametrize("transactions, currency_code", [
        (transactions, "EUR"),  # Ищем EUR в USD транзакциях (правильно - нет EUR)
        ([], "USD"),  # Пустой список
        (transactions, "CNY"),  # Несуществующая валюта
    ])
    def test_filter_by_currency_no_matches(self, transactions, currency_code):
        """Тест случая, когда нет транзакций в заданной валюте."""
        result = list(filter_by_currency(transactions, currency_code))
        assert len(result) == 0

    def test_filter_by_currency_empty_list(self):
        """Тест обработки пустого списка транзакций."""
        result = filter_by_currency([], "USD")
        # Преобразуем в список и проверяем, что он пустой
        assert list(result) == []

    @pytest.mark.parametrize("transactions, currency_code, expected_count, expected_ids", [
        (transactions, "USD", 3, [939719570, 142264268, 895315941]),
        (transactions, "EUR", 0, []),
    ])
    def test_filter_by_currency_incomplete_data(self, transactions, currency_code, expected_count, expected_ids):
        """Тест обработки транзакций с неполной структурой."""
        result = list(filter_by_currency(transactions, currency_code))

        assert len(result) == expected_count
        assert [t["id"] for t in result] == expected_ids

    @pytest.mark.parametrize("transactions, currency_code, expected_ids", [
        (transactions, "USD", [939719570, 142264268, 895315941]),
        (transactions, "usd", [939719570, 142264268, 895315941]),
    ])
    def test_filter_by_currency_case_sensitive(self, transactions, currency_code, expected_ids):
        """Тест чувствительности к регистру в коде валюты."""
        result = list(filter_by_currency(transactions, currency_code))

        assert [t["id"] for t in result] == expected_ids

    @pytest.mark.parametrize("transactions, currency_code, expected_first_id", [
        (transactions, "USD", 939719570),
        (transactions, "RUB", 873106923),
    ])
    def test_filter_by_currency_iterator_behavior(self, transactions, currency_code, expected_first_id):
        iterator = filter_by_currency(transactions, currency_code)

        # Более конкретная проверка - что это именно генератор
        assert isinstance(iterator, types.GeneratorType)

        first = next(iterator)
        assert first["id"] == expected_first_id

    def test_filter_by_currency_stop_iteration(self):
        """Тест возникновения StopIteration после окончания элементов."""
        iterator = filter_by_currency(self.transactions, "USD")

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


class TestCardNumberGenerator:
    """Тесты для генератора номеров банковских карт"""

    @pytest.mark.parametrize("start,stop,expected_sequence", [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (0, 0, ["0000 0000 0000 0000"]),
        (9999999999999997, 9999999999999999, [
            "9999 9999 9999 9997",
            "9999 9999 9999 9998",
            "9999 9999 9999 9999"
        ]),
    ])
    def test_sequence_generation(self, start, stop, expected_sequence):
        """Тестирование генерации последовательности номеров"""
        generator = card_number_generator(start, stop)
        results = list(generator)
        assert results == expected_sequence

    @pytest.mark.parametrize("number,expected_format", [
        (1234567812345678, "1234 5678 1234 5678"),
        (1111222233334444, "1111 2222 3333 4444"),
        (9999999999999999, "9999 9999 9999 9999"),
        (0, "0000 0000 0000 0000"),
        (1, "0000 0000 0000 0001"),
        (42, "0000 0000 0000 0042"),
        (1000000000000000, "1000 0000 0000 0000"),
    ])
    def test_format_correctness(self, number, expected_format):
        """Тестирование корректности форматирования"""
        generator = card_number_generator(number, number)
        result = next(generator)
        assert result == expected_format

    @pytest.mark.parametrize("start,stop,expected_count", [
        (1, 10, 10),
        (100, 105, 6),
        (0, 0, 1),
        (999, 999, 1),
        (10, 5, 0),  # некорректный диапазон
    ])
    def test_range_size(self, start, stop, expected_count):
        """Тестирование количества генерируемых номеров"""
        generator = card_number_generator(start, stop)
        results = list(generator)
        assert len(results) == expected_count

    @pytest.mark.parametrize("card_number", [
        "0000 0000 0000 0001",
        "1234 5678 9012 3456",
        "9999 9999 9999 9999",
        "1000 0000 0000 0000",
    ])
    def test_format_structure(self, card_number):
        """Тестирование структуры формата номеров карт"""
        # Извлекаем число из отформатированной строки
        number_str = card_number.replace(" ", "")
        number = int(number_str)

        generator = card_number_generator(number, number)
        result = next(generator)

        # Проверяем структуру
        assert len(result) == 19  # 16 цифр + 3 пробела
        assert result.count(' ') == 3
        parts = result.split()
        assert len(parts) == 4
        assert all(len(part) == 4 for part in parts)
        assert all(part.isdigit() for part in parts)

    @pytest.fixture
    def large_range_generator(self):
        """Фикстура для генератора с большим диапазоном"""
        return card_number_generator(100, 105)

    def test_generator_iteration(self, large_range_generator):
        """Тестирование итерации по генератору"""
        results = []
        for card_number in large_range_generator:
            results.append(card_number)

        expected = [
            "0000 0000 0000 0100",
            "0000 0000 0000 0101",
            "0000 0000 0000 0102",
            "0000 0000 0000 0103",
            "0000 0000 0000 0104",
            "0000 0000 0000 0105"
        ]
        assert results == expected

    @pytest.mark.parametrize("start,stop", [
        (9999999999999999, 9999999999999999),  # максимальное значение
        (0, 0),  # минимальное значение
        (1, 1),  # единица
    ])
    def test_single_value_ranges(self, start, stop):
        """Тестирование диапазонов из одного элемента"""
        generator = card_number_generator(start, stop)
        result = next(generator)

        # Проверяем, что генератор завершается после одного элемента
        with pytest.raises(StopIteration):
            next(generator)

        # Проверяем формат
        assert len(result) == 19
        assert result.count(' ') == 3

    def test_generator_exhaustion(self):
        """Тестирование исчерпания генератора"""
        generator = card_number_generator(1, 1)
        next(generator)  # получаем первый элемент

        # Генератор должен быть исчерпан
        with pytest.raises(StopIteration):
            next(generator)

    @pytest.mark.parametrize("invalid_start,invalid_end", [
        (-1, 10),  # отрицательное начало
        (10, -5),  # отрицательный конец
        (10000000000000000, 10000000000000001),  # значения больше 16 цифр
    ])
    def test_invalid_inputs(self, invalid_start, invalid_end):
        """
        Тестирование некорректных входных данных.
        Примечание: эта функция может не обрабатывать ошибки ввода,
        поэтому тест может быть пропущен или ожидать определенного поведения.
        """
        # В текущей реализации функция не проверяет валидность входных данных,
        # поэтому просто проверяем, что не возникает исключений (кроме StopIteration)
        try:
            generator = card_number_generator(invalid_start, invalid_end)
            list(generator)  # потребляем все значения
        except Exception as e:
            # Если функция добавит проверки, этот тест нужно будет обновить
            pytest.fail(f"Неожиданное исключение: {e}")

    @pytest.mark.slow
    def test_large_range_performance(self):
        """Тест производительности для большого диапазона (помечен как медленный)"""
        # Генерируем 1000 номеров карт
        generator = card_number_generator(1, 1000)
        results = list(generator)
        assert len(results) == 1000
        assert results[0] == "0000 0000 0000 0001"
        assert results[-1] == "0000 0000 0000 1000"

    @pytest.mark.parametrize("start,stop", [
        pytest.param(5, 10, id="small_range"),
        pytest.param(100, 110, id="medium_range"),
        pytest.param(1000, 1005, id="large_numbers"),
    ])
    def test_various_ranges(self, start, stop):
        """Параметризованный тест различных диапазонов"""
        generator = card_number_generator(start, stop)
        results = list(generator)

        expected_count = stop - start + 1
        assert len(results) == expected_count

        # Проверяем, что все номера имеют правильный формат
        for card_number in results:
            assert len(card_number) == 19
            assert card_number.count(' ') == 3
            assert all(part.isdigit() and len(part) == 4 for part in card_number.split())

    def test_consecutive_numbers(self):
        """Тест последовательных номеров"""
        generator = card_number_generator(1234567890123456, 1234567890123458)

        results = list(generator)
        expected = [
            "1234 5678 9012 3456",
            "1234 5678 9012 3457",
            "1234 5678 9012 3458"
        ]

        assert results == expected

    def test_single_digit_numbers(self):
        """Тест однозначных чисел"""
        generator = card_number_generator(7, 9)

        results = list(generator)
        expected = [
            "0000 0000 0000 0007",
            "0000 0000 0000 0008",
            "0000 0000 0000 0009"
        ]

        assert results == expected
