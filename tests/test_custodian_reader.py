import pytest
from conciliator.infrastructure.readers.custodian_reader import read_custodian_extract


def test_invalid_csv_schema(tmp_path):
    file = tmp_path / "data.csv"

    file.write_text("Wrong,Columns\n1,2")

    with pytest.raises(ValueError):
        read_custodian_extract(file)

def test_invalid_row(caplog, tmp_path):
    file = tmp_path / "data.csv"

    file.write_text(
        "Ativo,Quantidade,Saldo_Financeiro\n"
        "PETR4,abc,1000\n"
    )

    result = read_custodian_extract(file)

    assert len(result) == 0
    assert "Invalid custodian row skipped" in caplog.text

def test_negative_quantity(caplog, tmp_path):
    file = tmp_path / "data.csv"

    file.write_text(
        "Ativo,Quantidade,Saldo_Financeiro\n"
        "PETR4,-10,1000\n"
    )

    result = read_custodian_extract(file)

    assert len(result) == 0
    assert "Negative quantity" in caplog.text

def test_mixed_valid_invalid_rows(tmp_path):
    file = tmp_path / "data.csv"

    file.write_text(
        "Ativo,Quantidade,Saldo_Financeiro\n"
        "PETR4,100,1000\n"
        "VALE3,abc,2000\n"
    )

    result = read_custodian_extract(file)

    assert len(result) == 1
    assert result[0].quantity == 100