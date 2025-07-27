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
        # Обработка карты - возвращаем название с маскированным номером карты
        return f"{name} {get_mask_card_number(clean_number)}"


def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата "2024-03-11T02:26:18.671407"
    в формат 'ДД.ММ.ГГГГ'

    Аргументы:
        date_str: Строка с датой в формате ISO 8601 (YYYY-MM-DDTHH:MM:SS...)

    Возвращает:
        Строку с датой в формате ДД.ММ.ГГГГ

    Выбрасывает:
        ValueError: Если входная строка не соответствует ожидаемому формату
                   или содержит недопустимые значения даты
        IndexError: Если входная строка пустая
    """
    if not date_str:
        raise IndexError("Пустая строка даты")

    try:
        # Проверяем, может это вообще не дата в каком-либо формате
        if not any(c.isdigit() for c in date_str):
            raise ValueError("Неверный формат даты")

        # Сначала проверяем общий формат (наличие T и структуру даты)
        if "T" not in date_str:
            # Проверяем, не является ли это датой в другом формате (например, 31.12.2023)
            if "." in date_str or "/" in date_str:
                raise ValueError("Неверный формат даты")
            raise ValueError("Отсутствует разделитель 'T'")

        date_part = date_str.split("T")[0]
        parts = date_part.split("-")
        if len(parts) != 3:
            raise ValueError("Неверный формат даты")

        year_str, month_str, day_str = parts

        # Проверка что все компоненты состоят из цифр
        if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
            raise ValueError("Неверный формат даты")

        # Проверка длины (должны быть ведущие нули)
        if len(month_str) != 2 or len(day_str) != 2:
            raise ValueError("Требуются ведущие нули в дате")

        year = int(year_str)
        month = int(month_str)
        day = int(day_str)

        # Проверка года
        if year < 0:
            raise ValueError("Недопустимый год")

        # Проверка месяца
        if month < 1 or month > 12:
            raise ValueError("Недопустимый месяц")

        # Проверка дня
        if day < 1 or day > 31:
            raise ValueError("Недопустимый день")

        # Дополнительная проверка дня для месяцев с 30 днями
        if month in [4, 6, 9, 11] and day > 30:
            raise ValueError("Недопустимый день")

        # Проверка февраля с учетом високосных годов
        if month == 2:
            is_leap = (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0)
            if day > 29 or (day == 29 and not is_leap):
                raise ValueError("Недопустимый день")

        return f"{day_str}.{month_str}.{year_str}"

    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f"Неожиданная ошибка при обработке даты: {str(e)}")
