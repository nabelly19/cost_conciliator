"""
CSV report writer.
"""

import csv
from typing import List

from conciliator.domain.models.models import ReportEntry

def write_report(rows: List[ReportEntry], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Ticker",
            "Status",
            "Divergencia_Qtde",
            "Divergencia_Financ"
        ])
    
        for row in rows:
                writer.writerow([
                    row.ticker,
                    row.status,
                    row.divergence_quantity,
                    f"{row.divergence_value:.2f}"
                ])