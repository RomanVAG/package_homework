def filter_by_currency(transactions, currency_code):
    """
        Фильтрует транзакции по коду валюты и возвращает итератор.

        Args:
            transactions: список словарей с транзакциями
            currency_code: код валюты для фильтрации (например, "USD")

        Returns:
            итератор, который выдает транзакции с указанной валютой
    """
    for transaction in transactions:
        # Используем вложенные get() с значениями по умолчанию
        if transaction.get('operationAmount', {}).get('currency', {}).get('code') == currency_code:
            yield transaction


def transaction_descriptions(transactions):
    """
    Генератор, который возвращает описание каждой операции из списка транзакций.

    Args:
        transactions: список словарей с транзакциями

    Yields:
        строка с описанием операции
    """
    for transaction in transactions:
        # Проверяем наличие ключа 'description' в транзакции
        if 'description' in transaction:
            yield transaction['description']


def card_number_generator(start, end):
    """
    Генератор номеров банковских карт в заданном диапазоне.
    """
    for number in range(start, end + 1):
        # Форматируем число как 16-значную строку с нулями и добавляем пробелы
        card_str = f"{number:016d}"
        yield f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
