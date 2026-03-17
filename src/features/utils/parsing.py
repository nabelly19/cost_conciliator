"""
Utility functions for safe numeric parsing.
"""

from decimal import Decimal, InvalidOperation

def parse_decimal(value: str) -> Decimal:
    """
    Safely converts string values to Decimal.

    Handles both comma and dot decimal separators.

    Examples
    -

    35000.00
    35.000,00
    """

    if value is None:
        raise InvalidOperation("None value")

    cleaned = value.replace(".","").replace(",",".")

    return Decimal(cleaned)

def parse_int(value: str) -> int:
    """
    Safely converts numeric string to integer.
    """

    return int(value)