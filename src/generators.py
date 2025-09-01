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

