def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список операций по указанному статусу.

    Args:
        operations: Список операций (словарей с обязательным полем 'state')
        state: Статус для фильтрации ("EXECUTED" или "CANCELED"), по умолчанию "EXECUTED"

    Returns:
        Новый список операций, отфильтрованный по указанному статусу
    """
    sorted_list = []
    for operate in operations:
        if operate.get("state") == state:
            sorted_list.append(operate)
    return sorted_list


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список операций по дате.

    Args:
        operations: Список операций (словарей с обязательным полем 'date')
        reverse: Если True (по умолчанию) - сортировка по убыванию, False - по возрастанию

    Returns:
        Новый список операций, отсортированный по дате
    """
    sorted_list = sorted(operations, key=lambda x: x["date"], reverse=reverse)
    return sorted_list
