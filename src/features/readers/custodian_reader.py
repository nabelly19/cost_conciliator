"""
Reads the custodian CSV extract.
"""

import csv
from typing import List

from features.models.models import CustodianRecord
from features.utils.parsing import parse_decimal, parse_int
from features.utils.logging_config import get_logger

logger = get_logger(__name__)

REQUIRED_COLUMNS = {"Ativo", "Quantidade", "Saldo_Financeiro"}

def read_custodian_extract(path: str) -> List[CustodianRecord]:
    """
    Reads the custodian CSV extract.
    """

    records: List[CustodianRecord] = []

    with open(path, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        # --- validação de schema ---
        if not REQUIRED_COLUMNS.issubset(set(reader.fieldnames or [])):
            raise ValueError("Invalid CSV schema")

        for idx, row in enumerate(reader):

            try:
                name = row["Ativo"].strip()

                quantity = parse_int(row["Quantidade"])
                financial = parse_decimal(row["Saldo_Financeiro"])

                # --- validações de negócio ---
                if quantity < 0:
                    raise ValueError("Negative quantity")

                if financial < 0:
                    raise ValueError("Negative financial value")

                records.append(
                    CustodianRecord(
                        active_name=name,
                        quantity=quantity,
                        financial_value=financial,
                    )
                )

            except Exception as e:
                logger.warning(
                    "%s: Invalid custodian row skipped", str(e),
                    extra={"index": idx, "row": row, "error": str(e)}
                )

    logger.info("Loaded %s valid custodian records", len(records))

    return records