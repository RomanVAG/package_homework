from src.mask import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""
    if not isinstance(account_info, str):
        raise ValueError("Входные данные должны быть строкой")

    stripped = account_info.strip()
    if not stripped:
        return account_info

    parts = stripped.split()

    # Если только одно слово (название без номера)
    if len(parts) == 1:
        return account_info

    name = " ".join(parts[:-1])
    number = parts[-1]

    # Проверяем, содержит ли номер только цифры
    if not number.replace(" ", "").isdigit():
        raise ValueError("Номер должен содержать только цифры")

    try:
        if name.lower() == "счет":
            # Для счетов проверяем длину (20 цифр)
            if len(number) != 20:
                raise ValueError("Номер счета должен содержать 20 цифр")
            masked_number = get_mask_account(number)
        else:
            # Для карт сначала проверяем пробелы
            if " " in number:
                raise ValueError("Номер карты не должен содержать пробелов")
            # Затем проверяем длину (16 цифр)
            if len(number) != 16:
                raise ValueError("Номер карты должен содержать 16 цифр")
            masked_number = get_mask_card_number(number)
    except ValueError as e:
        raise ValueError(str(e))

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
