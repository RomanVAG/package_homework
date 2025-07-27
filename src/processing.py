def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Принимает список словарей. Имеет необязательный параметр
    для порядка сортировки (по умолчанию EXECUTED — выполнено,
    либо CANCELED — отменено).  Возвращает новый список,
    отсортированный по статусу (state).
    """
    sorted_list = []
    for operate in operations:
        if operate.get("state") == state:
            sorted_list.append(operate)
    return sorted_list


def sort_by_date(operations: list[dict], reverse=True) -> list[dict]:
    """
    Принимает список словарей. Имеет необязательный параметр `reverse`,
    задающий порядок сортировки:
    reverse=True (по умолчанию) — сортировка по убыванию даты,
    reverse=False — сортировка по возрастанию даты.
    Возвращает новый список, отсортированный по ключу - date.
    """
    sorted_list = sorted(operations, key=lambda x: x["date"], reverse=reverse)
    return sorted_list
