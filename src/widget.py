from src.mask import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в переданной строке.
    """
    # Проверка типа входных данных
    if not isinstance(account_info, str):
        raise ValueError("Входные данные должны быть строкой")

    # Удаление лишних пробелов по краям
    stripped = account_info.strip()
    # Если строка пустая после удаления пробелов, возвращаем исходную строку
    if not stripped:
        return account_info

    # Разделяем строку на название и номер
    # находим индекс первого цифрового символа - начало номера
    first_digit_pos = None
    for i, char in enumerate(stripped):
        if char.isdigit():
            first_digit_pos = i
            break

    # Если не нашли цифр в строке, возвращаем исходную строку
    if first_digit_pos is None:
        return account_info

    # Разделяем на название (все до первой цифры) и номер (все цифры и пробелы между ними)
    name = stripped[:first_digit_pos].strip()
    number = stripped[first_digit_pos:]

    # Удаляем все пробелы из номера для последующих проверок
    clean_number = number.replace(" ", "")

    # Проверяем, является ли продукт счетом
    if "счет" in name.lower():
        # Обработка счета - возвращаем название с маскированным номером счета
        return f"{name} {get_mask_account(clean_number)}"
    else:
        # Обработка карты - получаем маскированный номер (без пробелов)
        masked_number = get_mask_card_number(clean_number)
        # Возвращаем название с маскированным номером карты
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
