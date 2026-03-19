"""
Data models used across the reconciliation system.

Using dataclasses ensures:
- strong typing
- immutability options
- easy serialization
"""

from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Position:
    """
    Represents a position in the internal system.
    """
    ticker: str
    quantity: int
    financial_value: Decimal
    
@dataclass
class CustodianRecord:
    """
    Represents a record from the custodian's data.
    """
    active_name: str
    quantity: int
    financial_value: Decimal
    
@dataclass
class ReportEntry:
    """
    Represents a single entry in the reconciliation report.
    """
    ticker: str
    status: str
    divergence_quantity: int
    divergence_value: Decimal