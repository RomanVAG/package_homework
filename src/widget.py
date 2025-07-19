from src.mask import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""
    if not account_info.strip():  # Если строка пустая или содержит только пробелы
        return account_info

    parts = account_info.split()
    if not parts:  # На всякий случай (хотя предыдущая проверка это уже отсекает)
        return account_info

    name = " ".join(parts[:-1]) if len(parts) > 1 else parts[0]
    number = parts[-1] if len(parts) > 1 else ""

    # Если нет номера (только "Счет" или "Карта"), возвращаем как есть
    if not number:
        return account_info

    # Маскируем в зависимости от типа
    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}" if name else masked_number


def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата "2024-03-11T02:26:18.671407"
    в формат 'ДД.ММ.ГГГГ'
    """
    # Разделяем строку по 'T' и берем первую часть (дату)
    date_part = date_str.split("T")[0]
    # Разделяем дату по '-'
    year, month, day = date_part.split("-")
    # Форматируем в нужный вид
    return f"{day}.{month}.{year}"
