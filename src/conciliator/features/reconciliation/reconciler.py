"""
Core reconciliation engine.
"""

from decimal import Decimal
from typing import Dict, List

from models.models import Position, CustodianRecord, ReportRow
from mapping.ticker_mapper import TickerMapper

TOLERANCE = Decimal("0.01")

def reconcile(
    internal: Dict[str, Position],
    custodian: List[CustodianRecord],
    mapper: TickerMapper
) -> List[ReportRow]:

    custodian_map = {}

    for record in custodian:

        ticker = mapper.map_to_ticker(record.active_name)

        if ticker is None:
            continue

        custodian_map[ticker] = record

    report: List[ReportRow] = []

    for ticker, position in internal.items():
        if ticker not in custodian_map:
            report.append(
                ReportRow(
                    ticker=ticker,
                    status="FALTANTE_NO_BANCO",
                    divergence_quantity=-position.quantity,
                    divergence_value=-position.financial_value
                )
            )

            continue

        custodian = custodian_map[ticker]

        dq = custodian.quantity - position.quantity
        dv = custodian.financial_value - position.financial_value

        if dq != 0:
            status = "ERRO_QUANTIDADE"
        
        elif abs(df) >= TOLERANCE:
            status = "ERRO_FINANCEIRO"
        
        else:
            status = "OK"

        report.append(
            ReportRow(
                ticker=ticker,
                status=status,
                divergence_quantity=dq,
                divergence_value= dv
            )
        )

    return report