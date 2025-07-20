from src.mask import get_mask_account, get_mask_card_number

def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в переданной строке.
    Для карт используется маска: первые 4 цифры, затем ** и последние 4 цифры
    Для счетов отображается только ** и последние 4 цифры
    """
    # Проверяем тип входных данных
    if not isinstance(account_info, str):
        raise ValueError("Входные данные должны быть строкой")

    # Сохраняем оригинальное форматирование пробелов
    leading_spaces = account_info[:len(account_info) - len(account_info.lstrip())]
    trailing_spaces = account_info[len(account_info.rstrip()):]

    # Очищаем строку для обработки
    stripped_info = account_info.strip()

    # Разделяем на части
    parts = stripped_info.split()

    # Если строка пустая или содержит только пробелы
    if not parts:
        return account_info

    # Определяем тип счета/карты
    is_account = any(word.lower() in ['счет', 'счёт'] for word in parts)

    # Ищем номер (последняя последовательность цифр)
    number = ''
    name_parts = []
    for part in parts:
        if part.isdigit():
            number = part
        else:
            name_parts.append(part)

    # Если номер не найден, возвращаем исходную строку
    if not number:
        return account_info

    # Проверяем, что номер состоит только из цифр
    if not number.isdigit():
        raise ValueError("Номер должен содержать только цифры")

    # Проверяем наличие пробелов в номере карты
    if not is_account and ' ' in number:
        raise ValueError("Номер карты не должен содержать пробелов")

    # Маскируем в зависимости от типа
    if is_account:
        # Для счетов: ** + последние 4 цифры
        if len(number) >= 4:
            masked_number = f"**{number[-4:]}"
        else:
            masked_number = number
    else:
        # Для карт: 4 + ** + ** + ** + 4
        if len(number) == 16:
            masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
        else:
            masked_number = number

    # Собираем результат, сохраняя оригинальное форматирование
    name_part = ' '.join(name_parts)
    original_space = ' ' if name_part and number else ''

    return f"{leading_spaces}{name_part}{original_space}{masked_number}{trailing_spaces}"


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
