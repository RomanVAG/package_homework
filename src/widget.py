from src.mask import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""
    if not isinstance(account_info, str):
        raise ValueError("Входные данные должны быть строкой")

    # Удаляем лишние пробелы и разделяем строку на части
    stripped = account_info.strip()
    if not stripped:
        return account_info

    parts = stripped.split()

    # Если только одно слово (название без номера)
    if len(parts) == 1:
        return account_info

    # Собираем название (все части кроме последней)
    name = " ".join(parts[:-1])
    number = parts[-1]

    # Маскируем в зависимости от типа
    try:
        if name.lower() == "счет":
            masked_number = get_mask_account(number)
        else:
            masked_number = get_mask_card_number(number)
    except ValueError:
        # Если номер невалидный, возвращаем исходную строку
        return account_info

    return f"{name} {masked_number}"


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
