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
    Преобразует дату из формата ISO 8601 ("YYYY-MM-DDThh:mm:ss...")
    в формат 'ДД.ММ.ГГГГ'.

    Args:
        date_str: Строка с датой в формате ISO 8601 (обязательно с 'T')

    Returns:
        Строка с датой в формате 'ДД.ММ.ГГГГ'

    Raises:
        ValueError: Если входная строка имеет неверный формат или недопустимую дату
        IndexError: Если строка пустая или не содержит компонентов даты
    """
    if not date_str:
        raise IndexError("Пустая строка даты")

    if 'T' not in date_str:
        raise ValueError("Отсутствует разделитель 'T' между датой и временем")

    try:
        date_part = date_str.split('T')[0]
        parts = date_part.split('-')

        if len(parts) != 3:
            raise ValueError("Неверный формат даты. Ожидается YYYY-MM-DD")

        year, month, day = parts

        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            raise ValueError("Все компоненты даты должны быть цифрами")

        year_num = int(year)
        month_num = int(month)
        day_num = int(day)

        if month_num < 1 or month_num > 12:
            raise ValueError(f"Недопустимый месяц: {month_num}. Должен быть 1-12")

        if day_num < 1:
            raise ValueError(f"Недопустимый день: {day_num}. День не может быть меньше 1")

        # Проверка максимального количества дней в месяце
        max_days = 31
        if month_num in [4, 6, 9, 11]:
            max_days = 30
        elif month_num == 2:
            max_days = 29 if (year_num % 400 == 0 or (year_num % 100 != 0 and year_num % 4 == 0)) else 28

        if day_num > max_days:
            raise ValueError(f"Недопустимый день {day_num} для месяца {month_num}. Максимум {max_days}")

        # Форматирование с ведущими нулями
        day_str = f"{day_num:02d}"
        month_str = f"{month_num:02d}"

        return f"{day_str}.{month_str}.{year}"

    except IndexError as e:
        raise IndexError("Не удалось разобрать строку даты") from e
