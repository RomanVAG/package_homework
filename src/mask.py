def get_mask_card_number(card_number: str | int) -> str:
    """Маскирует номер банковской карты (цифры с 7 по 12)"""
    if not isinstance(card_number, (str, int)) or isinstance(card_number, bool):
        raise ValueError("Номер карты должен быть строкой или числом")

    card_str = str(card_number).replace(" ", "")  #

    if not card_str or not card_str.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    if len(card_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"


def get_mask_account(account: str | int) -> str:
    """Маскирует номер банковского счёта (первые 12 цифр)"""
    if account is None:
        raise ValueError("Номер счета не может быть пустым")

    if not isinstance(account, (str, int)):
        raise ValueError("Номер счета должен быть строкой или числом")

    account_str = str(account).strip()

    if not account_str or not account_str.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    if len(account_str) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр")

    return f"**{account_str[-4:]}"