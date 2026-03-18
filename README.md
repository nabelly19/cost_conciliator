## Project Structure
```
src/
  main.py                          # Entry point - orchestrates the full flow
  conciliator/features/
    mapping/ticker_mapper.py       # Maps custodian asset names to internal tickers
    models/models.py               # Data models: Position, CustodianRecord, ReportEntry
    readers/
      internal_reader.py           # Reads internal JSON positions file
      custodian_reader.py          # Reads custodian CSV extract
    reconciliation/reconciler.py   # Core reconciliation engine
    utils/
      logging_config.py            # Centralized logging setup
      parsing.py                   # Safe numeric parsing (handles BR/EN formats)
    writers/report_writer.py       # Writes CSV reconciliation report
  data/
    input/
      internal_system.json         # Internal system positions (Portuguese field names)
      custodian_extract.csv        # Custodian extract (Portuguese column headers)
    output/
      relatorio_final.csv          # Generated reconciliation report
tests/
  test_mapper.py
  test_reconciliation.py
```

## Setup & Running

- **Language**: Python 3.12
- **Testing**: pytest (installed via uv)
- **Python path**: `src` and `src/conciliator/features` are both on the path (configured in `pytest.ini`)

### Run reconciliation
```bash
cd src && PYTHONPATH=/home/runner/workspace/src:/home/runner/workspace/src/conciliator/features python3 main.py
```

### Run tests
```bash
python3 -m pytest tests/ -v
```

## Key Design Decisions

- Uses `Decimal` for financial calculations (avoids floating point errors)
- `parse_decimal` detects whether the number uses comma or dot as decimal separator
- `TickerMapper` normalizes company names (strips "S.A.", "HOLDING", extra spaces) for fuzzy matching
- Tolerance for financial comparison is `0.01`
- Report statuses: `OK`, `ERRO_QUANTIDADE`, `ERRO_FINANCEIRO`, `FALTANTE_NO_BANCO`