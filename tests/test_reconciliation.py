from decimal import Decimal
from conciliator.domain.services.reconciliation.reconciler import reconcile
from conciliator.domain.models.models import Position, CustodianRecord
from conciliator.domain.mapping.ticker_mapper import TickerMapper

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

def test_status_ok():
    internal = {
        "PETR4": Position("PETR4", 100, Decimal("1000"))
    }

    custodian = [
        CustodianRecord("PETROLEO BRASILEIRO S.A.", 100, Decimal("1000"))
    ]

    result = reconcile(internal, custodian, TickerMapper())

    assert result[0].status == "OK"

def test_status_erro_quantidade():
    internal = {
        "VALE3": Position("VALE3", 100, Decimal("1000"))
    }

    custodian = [
        CustodianRecord("VALE S.A.", 90, Decimal("900"))
    ]

    result = reconcile(internal, custodian, TickerMapper())

    assert result[0].status == "ERRO_QUANTIDADE"

def test_status_erro_financeiro():
    internal = {
        "ITUB4": Position("ITUB4", 100, Decimal("1000"))
    }

    custodian = [
        CustodianRecord("ITAU UNIBANCO HOLDING S.A.", 100, Decimal("1000.02"))
    ]

    result = reconcile(internal, custodian, TickerMapper())

    assert result[0].status == "ERRO_FINANCEIRO"

def test_status_faltante_no_banco():
    internal = {
        "BBDC4": Position("BBDC4", 100, Decimal("1000"))
    }

    custodian = []

    result = reconcile(internal, custodian, TickerMapper())

    assert result[0].status == "FALTANTE_NO_BANCO"

def test_status_nao_cadastrado():
    internal = {}

    custodian = [
        CustodianRecord("KNIP11", 100, Decimal("1000"))
    ]

    result = reconcile(internal, custodian, TickerMapper())

    assert result[0].status == "NAO_CADASTRADO"