import pytest
from features.readers.internal_reader import read_internal_positions


def test_internal_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_internal_positions("arquivo_inexistente.json")

def test_invalid_json(tmp_path):
    file = tmp_path / "invalid.json"
    file.write_text("{ invalid json }")

    with pytest.raises(Exception):
        read_internal_positions(file)

def test_missing_fields(caplog, tmp_path):
    file = tmp_path / "data.json"

    file.write_text("""
    [
        {"ticker": "PETR4", "quantidade": 100}
    ]
    """)

    result = read_internal_positions(file)

    assert len(result) == 0
    assert "Invalid internal record skipped" in caplog.text

    def test_invalid_quantity(caplog, tmp_path):
    file = tmp_path / "data.json"

    file.write_text("""
    [
        {"ticker": "PETR4", "quantidade": "abc", "financeiro": 1000}
    ]
    """)

    result = read_internal_positions(file)

    assert len(result) == 0
    assert "Invalid internal record skipped" in caplog.text

    def test_negative_values(caplog, tmp_path):
    file = tmp_path / "data.json"

    file.write_text("""
    [
        {"ticker": "PETR4", "quantidade": -10, "financeiro": 1000}
    ]
    """)

    result = read_internal_positions(file)

    assert len(result) == 0
    assert "Negative quantity" in caplog.text

    def test_duplicate_ticker(caplog, tmp_path):
    file = tmp_path / "data.json"

    file.write_text("""
    [
        {"ticker": "PETR4", "quantidade": 100, "financeiro": 1000},
        {"ticker": "PETR4", "quantidade": 200, "financeiro": 2000}
    ]
    """)

    result = read_internal_positions(file)

    assert len(result) == 1
    assert result["PETR4"].quantity == 200
    assert "Duplicate ticker" in caplog.text

    