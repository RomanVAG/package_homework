def get_mask_card_number(card_number: str | int) -> str:
    """Маскирует номер банковской карты (цифры с 7 по 12)"""
    if not isinstance(card_number, (str, int)) or isinstance(card_number, bool):
        raise ValueError("Номер карты должен быть строкой или числом")

    card_str = str(card_number).strip()

    if not card_str:
        raise ValueError("Номер карты должен содержать 16 цифр")

    if not card_str.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    if len(card_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"


def get_mask_account(account: str | int) -> str:
    """Маскирует номер банковского счёта (первые 12 цифр)"""
    if account is None:
        raise ValueError("Номер счета не может быть None")

    # Явно проверяем что тип именно str или int, а не bool
    if isinstance(account, bool) or not isinstance(account, (str, int)):
        raise ValueError("Номер счета должен быть строкой или числом")

    account_str = str(account).strip()

    # Отдельная проверка на пустую строку
    if not account_str:
        raise ValueError("Номер счета не может быть пустым")

    # Проверка что строка состоит только из цифр
    if not account_str.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    # Проверка длины счета (20 цифр)
    if len(account_str) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр")

    # Маскировка (первые 16 цифр заменяются на *)
    return f"**{account_str[-4:]}"
