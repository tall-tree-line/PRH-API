from datetime import datetime
from typing import Optional
import re

def as_timestamp(string:str|None) -> datetime|None:
    if not string:
        return None
    return datetime.strptime(string, '%Y-%m-%d')

SOURCE_MAPPING = {
    0:"common",
    1:"prh",
    2:"tax-administration",
    3:"business-registry"
}

REGISTERED_ENTRY_STATUS = {
    0:"common",
    1:"unregistered",
    2:"registered"
}

REGISTERED_ENTRY_REGISTER = {
    1:"trade-register",
    2:"foundation-register",
    3:"association-register",
    4:"tax-administration",
    5:"prepayment-register",
    6:"vat-register",
    7:"employer-register",
    8:"insurance-register",
}

REGISTERED_ENTRY_AUTHORITY = {
    1:"tax-administration",
    2:"prh",
    3:"population-register"
}

def convert_source(source:Optional[int]) -> Optional[str]:
    return SOURCE_MAPPING.get(source) if source else None

def convert_version(version:Optional[int]) -> Optional[str]:
    if not version:
        return
    return "current" if version == 0 else "former"

def convert_address_type(value:int) -> Optional[int]:
    if not value:
        return
    address_types = {
        1:"physical_address",
        2:"mailing_address"
    }
    return address_types.get(value)

def is_valid_company_number(s: str) -> bool:
    """
    Checks if a string is in the format: first 7 characters are numbers, then a dash, and then a number again.
    The total length of the string should be 9, which contains 8 numbers and a dash as the 8th character.

    Args:
        s (str): The string to check. A finnish company_number.

    Returns:
        bool: True if the string is in the correct format, False otherwise.
    """
    pattern = r'^\d{7}-\d$'
    return bool(re.match(pattern, s))
