"""
Ticker mapping logic.

Responsible for translating custodian asset names
into internal system tickers.

Implements heuristic fallback matching.
"""

import re
from typing import Optional, Dict

from features.utils.logging_config import get_logger

logger = get_logger(__name__)

class TickerMapper:
    """
    Handles mapping between custodian names and internal tickers.
    """

    def __init__(self) -> None:

        self.explicit_map: Dict[str, str] = {
            "PETROLEO BRASILEIRO S.A.": "PETR4",
            "VALE S.A.": "VALE3",
            "ITAU UNIBANCO HOLDING S.A.": "ITUB4",
            "MAGAZINE LUIZA S.A.": "MGLU3",
            "WEG S.A.": "WEGE3",
        }

    def normalize_name(self, name: str) -> str:
        """
        Normalize company names removing legal suffixes.
        """

        name = name.upper()

        name = re.sub(r"S\.\s*A\.", "", name)
        name = re.sub(r"HOLDING", "", name)

        name = re.sub(r"\s+", " ", name)

        return name.strip()

    def is_probable_ticker(self, value: str) -> bool:
        """
        Detects if a string already looks like a ticker.
        Example: KNIP11
        """

        return bool(re.match(r"^[A-Z]{4}\d{2,}", value)) 

    def map_to_ticker(self, name: str) -> Optional[str]:
        """
        Attempts to map a custodian name to a ticker.
        """

        if name in self.explicit_map:
            return self.explicit_map[name]

        normalized = self.normalize_name(name)

        for key, ticker in self.explicit_map.items():

            if self.normalize_name(key) == normalized:
                return ticker

        if self.is_probable_ticker(name):
            return name

        logger.warning("Unable to map asset: %s", name)

        return None
