"""
Reads the custodian CSV extract.
"""

import csv
from typing import List

from models.models import CustodianRecord
from utils.parsing import parse_decimal, parse_int
from utils.logging_config import get_logger

logger = get_logger(__name__)

def read_custodian_extract(path: str) -> List[CustodianRecord]:
    """
    Reads the custodian CSV extract.
    """

    records: List[CustodianRecord] = []

    with open(path, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:
            try:
                record = CustodianRecord(
                    active_name=row["Active"],
                    quantity=parse_int(row["Quantity"]),
                    financial_value=parse_decimal(row["Financial Balance"]),
                )

                records.append(record)

            except Exception as e:
                logger.warning("Skipping invalid row: %s", e)

        logger.info("Loaded %s custodian records", len(records))

        return record