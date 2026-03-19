"""
Reads the custodian CSV extract.
"""

import csv
from typing import List

from features.models.models import CustodianRecord
from features.utils.parsing import parse_decimal, parse_int
from features.utils.logging_config import get_logger

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
                    active_name=row["Ativo"],
                    quantity=parse_int(row["Quantidade"]),
                    financial_value=parse_decimal(row["Saldo_Financeiro"]),
                )

                records.append(record)

            except Exception as e:
                logger.warning("Skipping invalid row: %s", e)

    logger.info("Loaded %s custodian records", len(records))

    return records