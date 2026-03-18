"""
Reads the internal system JSON file.
"""

import json
from pathlib import Path
from typing import Dict
from decimal import Decimal

from models.models import Position
from utils.logging_config import get_logger

logger = get_logger(__name__)

def read_internal_positions(path: str) -> Dict[str, Position]:
    """
    Reads the internal JSON system file.

    Returns
    -
    Dict[str, Position]
        Keyed by ticker
    """

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Internal file not found: {path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    positions: Dict[str, Position] = {}

    for record in data:

        ticker = record["ticker"].upper()

        positions[ticker] = Position(
            ticker=ticker,
            quantity=int(record["quantidade"]),
            financial_value=Decimal(str(record["financeiro"]))
        )

    logger.info("Loaded %s positions from internal system", len(positions))

    return positions