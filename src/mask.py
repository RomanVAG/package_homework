def get_mask_card_number(card_number: str | int) -> str:
    """Маскирует номер банковской карты (цифры с 7 по 12)"""

    # Сначала проверяем тип данных (включая bool, так как bool является подклассом int)
    if type(card_number) not in (str, int) or isinstance(card_number, bool):
        raise ValueError("Номер карты должен быть строкой или числом")

    # Преобразуем в строку
    card_str = str(card_number)

    # Проверка на пустую строку
    if not card_str:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Проверка, что все символы - цифры
    if not card_str.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    # Проверка длины
    if len(card_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Маскировка номера
    return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"


def get_mask_account(account: str | int) -> str:
    """Маскирует номер банковского счёта (первые 12 цифр)"""
    if account is None:
        raise ValueError("Номер счета не может быть None")

    if not isinstance(account, (str, int)) or isinstance(account, bool):
        raise ValueError("Номер счета должен быть строкой или числом")

    account_str = str(account)

    if not account_str:
        raise ValueError("Номер счета не может быть пустым")

    if not account_str.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    return f"**{account_str[-4:]}"
