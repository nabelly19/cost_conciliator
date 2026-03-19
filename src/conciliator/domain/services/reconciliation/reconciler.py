"""
Core reconciliation engine.
"""

from decimal import Decimal
from typing import Dict, List

from conciliator.domain.models.models import Position, CustodianRecord, ReportEntry
from conciliator.domain.mapping.ticker_mapper import TickerMapper

TOLERANCE = Decimal("0.01")

def reconcile(
    internal: Dict[str, Position],
    custodian: List[CustodianRecord],
    mapper: TickerMapper,
) -> List[ReportEntry]:
    custodian_map = {}

    for record in custodian:
        ticker = mapper.map_to_ticker(record.active_name)

        if ticker is None:
            continue

        custodian_map[ticker] = record

    report: List[ReportEntry] = []

    for ticker, position in internal.items():
        if ticker not in custodian_map:
            report.append(
                ReportEntry(
                    ticker=ticker,
                    status="FALTANTE_NO_BANCO",
                    divergence_quantity=-position.quantity,
                    divergence_value=-position.financial_value,
                )
            )

            continue

        custodian_record = custodian_map[ticker]

        dq = custodian_record.quantity - position.quantity
        dv = custodian_record.financial_value - position.financial_value

        if dq != 0:
            status = "ERRO_QUANTIDADE"

        elif abs(dv) >= TOLERANCE:
            status = "ERRO_FINANCEIRO"

        else:
            status = "OK"

        report.append(
            ReportEntry(
                ticker=ticker,
                status=status,
                divergence_quantity=dq,
                divergence_value=dv,
            )
        )

    for ticker, custodian_record in custodian_map.items():
        if ticker not in internal:
            report.append(
                ReportEntry(
                    ticker=ticker,
                    status="NAO_CADASTRADO",
                    divergence_quantity=custodian_record.quantity,
                    divergence_value=custodian_record.financial_value,
                )
            )

    return report
