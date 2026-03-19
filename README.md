## Cost Conciliator

A Python-based reconciliation tool designed to compare internal system positions with custodian records, identifying discrepancies in quantity and financial values.

## Project Structure
```
cost_conciliator/ 
│
├── src/ 
│ ├── main.py 
│ ├── features/ 
│ │ ├── mapping/ 
│ │ ├── models/ 
│ │ ├── readers/ 
│ │ ├── reconciliation/ 
│ │ ├── utils/ 
│ │ └── writers/ 
│ └── data/ 
│   ├── input/ 
│   └── output/ 
|
├── tests/ 
├── setup.py 
├── README.md 
└── pytest.ini

```

## Requirements

- **Language**: Python 3.10+
- **Package Manager**: pip

### Install Dependencies

Install the project in editable mode:
```bash
pip install -e .
```

## Input Data

Place your input files in:

```bash
src/data/input/
```

### Required files:

1. Internal System (JSON)
2. Custodian Extract (CSV)

## Running the Application

From the project root directory, run:

```bash
python -m src.main
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