from features.mapping.ticker_mapper import TickerMapper

def test_explicit_mapping():
    mapper = TickerMapper()

    assert mapper.map_to_ticker(
        "PETROLEO BRASILEIRO S.A."
    ) == "PETR4"