"""
Reads the internal system JSON file.
"""

import json
from pathlib import Path
from typing import Dict
from decimal import Decimal, InvalidOperation

from features.models.models import Position
from features.utils.logging_config import get_logger

logger = get_logger(__name__)

REQUIRED_FIELDS = {"ticker", "quantidade", "financeiro"}

def read_internal_positions(path: str) -> Dict[str, Position]:
    """
    Reads and validates internal system JSON data.

    Returns
    -
    Dict[str, Position]
        Keyed by ticker
    """

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Internal file not found: {path}")

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON format", extra={"error": str(e)})
            raise

    positions: Dict[str, Position] = {}

    for idx, record in enumerate(data):

        try:

            if not REQUIRED_FIELDS.issubset(record):
                raise ValueError(f"Missing fields: {REQUIRED_FIELDS - record.keys()}")

            ticker = str(record["ticker"]).strip().upper()

            quantity = int(record["quantidade"])
            financial = Decimal(str(record["financeiro"]))

            if quantity < 0:
                raise ValueError("Negative quantity")

            if financial < 0:
                raise ValueError("Negative financial value")

            if ticker in positions:
                logger.warning(
                    "Duplicate ticker found, overwriting",
                    extra={"ticker": ticker}
                )

            positions[ticker] = Position(
                ticker=ticker,
                quantity=quantity,
                financial_value=financial
            )

        except (ValueError, InvalidOperation, TypeError) as e:
            logger.warning(
                "%s: Invalid internal record skipped", str(e),
                extra={"index": idx, "record": record, "error": str(e)}
            )

    logger.info("Loaded %s valid positions", len(positions))

    return positions