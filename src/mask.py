def get_mask_card_number(card_number: str | int) -> str:
    """Маскирует номер банковской карты (цифры с 7 по 12)"""
    card_str = str(card_number)
    return f"{card_str[:4]} {card_str[4:6]}XX XXXX {card_str[-4:]}"


def get_mask_account(account: str | int) -> str:
    """Маскирует номер банковского счёта (первые 12 цифр)"""
    account_str = str(account)
    return f"**{account_str[-4:]}"
