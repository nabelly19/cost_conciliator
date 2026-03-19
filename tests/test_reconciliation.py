from decimal import Decimal
from features.reconciliation.reconciler import reconcile
from features.models.models import Position, CustodianRecord
from features.mapping.ticker_mapper import TickerMapper

def test_quantity_error():
    internal = {
        "VALE3" : Position("VALE3", 500, Decimal("32500"))
    }

    custodian = [
        CustodianRecord("VALE S. A.", 490, Decimal("31850"))
    ]

    mapper = TickerMapper()

    result = reconcile(internal, custodian, mapper)

    assert result[0].status == "ERRO_QUANTIDADE"