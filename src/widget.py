from src.mask import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""
    if not account_info.strip():  # Если строка пустая или содержит только пробелы
        return account_info

    # Сохраняем исходные пробелы
    leading_spaces = account_info[:len(account_info) - len(account_info.lstrip())]
    trailing_spaces = account_info[len(account_info.rstrip()):]

    # Работаем с очищенной строкой (без ведущих/конечных пробелов)
    clean_str = account_info.strip()
    parts = clean_str.split()

    if not parts:
        return account_info

    # Разделяем название и номер
    name_parts = []
    number = ""
    for part in parts:
        if part.isdigit():
            number = part
            break
        name_parts.append(part)

    name = " ".join(name_parts) if name_parts else ""

    # Если нет номера или номер слишком короткий
    if not number or (name.lower() == "счет" and len(number) < 4) or (name.lower() != "счет" and len(number) != 16):
        return account_info

    # Маскируем номер
    if name.lower() == "счет":
        masked_number = f"**{number[-4:]}"
    else:
        masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"

    # Восстанавливаем оригинальные пробелы между названием и номером
    original_parts = account_info.split()
    if len(original_parts) > 1:
        # Находим позицию начала номера в исходной строке
        num_start = account_info.find(original_parts[-1])
        # Вычисляем пробелы между названием и номером
        space_between = account_info[len(leading_spaces) + len(' '.join(original_parts[:-1])):num_start]
    else:
        space_between = " "

    # Собираем результат с сохранением всех пробелов
    result = f"{leading_spaces}{name}{space_between}{masked_number}{trailing_spaces}"
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
