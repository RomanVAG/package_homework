def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в переданной строке.

    Параметры:
        account_info: строка формата "Visa Platinum 7000792289606361" или "Счет 73654108430135874305"

    Возвращает:
        Строку с замаскированным номером (карта: XXXX XX** **** XXXX, счет: **XXXX)
    """
    # Разделяем строку на части
    parts = account_info.split()

    # Определяем тип (карта или счет)
    if not parts:
        return account_info

    # Собираем название (все части кроме последней)
    name = " ".join(parts[:-1])
    number = parts[-1]

    # Маскируем в зависимости от типа
    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_mask_card_number(card_number: str | int) -> str:
    """Маскирует номер банковской карты (цифры с 7 по 12)"""
    card_str = str(card_number)
    return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"


def get_mask_account(account: str | int) -> str:
    """Маскирует номер банковского счёта (первые 12 цифр)"""
    account_str = str(account)
    return f"**{account_str[-4:]}"


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
