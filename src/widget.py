from src.mask import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""

    # Проверка, является ли переданный аргумент строкой. Если нет — генерируется исключение ValueError
    if not isinstance(account_info, str):
        raise ValueError("Входные данные должны быть строкой")

    # Удаляем пробелы в начале и конце строки.
    # Еcли строка пустая, либо состоит только из пробелов, возвращаем исходную строку без изменений.
    if not account_info.strip():
        return account_info

    # Сохраняем пробелы в начале и конце
    leading_spaces = account_info[:len(account_info) - len(account_info.lstrip())]
    trailing_spaces = account_info[len(account_info.rstrip()):]

    # Разделяем на слова (без лишних пробелов)
    parts = account_info.strip().split()
    if not parts:
        return account_info

    # Находим номер (последняя последовательность цифр)
    number = ''
    name_parts = []
    for part in reversed(parts):
        if part.isdigit():
            number = part
            break
        name_parts.insert(0, part)

    # Если номер не найден, возвращаем исходную строку
    if not number:
        return account_info

    # Проверяем, что номер состоит только из цифр
    if not number.isdigit():
        raise ValueError("Номер должен содержать только цифры")

    # Проверяем наличие пробелов в номере
    is_account = any(word.lower() in ['счет', 'счёт'] for word in name_parts)
    if not is_account and ' ' in number:
        raise ValueError("Номер не должен содержать пробелов")

    # Проверка длины
    if len(number) not in (16, 20):
        raise ValueError("Номер карты или номер счета должен содержать 16 или 20 цифр")

    # Маскировка
    if is_account:
        masked_number = f"**{number[-4:]}"
    else:
        masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"

    # Собираем результат с сохранением оригинального форматирования
    name_part = ' '.join(name_parts) if name_parts else ""
    original_space = ' ' if name_part else ""

    result = f"{leading_spaces}{name_part}{original_space}{masked_number}{trailing_spaces}"
    return result


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
