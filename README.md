# Custody Reconciliation System

A Python-based reconciliation tool designed to compare internal portfolio positions with custodian records, identifying discrepancies in quantity and financial values.

---
## Architecture

The project follows a modular architecture inspired by clean architecture principles:

```
src/
└── conciliator/
├── domain/ # Business logic
│ ├── models/
│ ├── services/ # Reconciliation logic
│ ├── mapping/ # Ticker mapping (heuristics)
│ └── enums/
│
├── infrastructure/ # I/O layer
│ ├── readers/
│ └── writers/
│
├── utils/ # Shared utilities
└── main.py # Entry point
```

---

## Data

Input and output files are stored outside the source code:

```
data/
├── input/
│ ├── internal_system.json
│ └── custodian_extract.csv
│
└── output/
  └── relatorio_final.csv
```

---

## Requirements

- **Language**: Python 3.10+ 
- **Package Manager**: pip

## Installation

Install the project in editable mode:

```bash
pip install -e .
```

```bash
pip install pytest
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Running the Application

From the project root:

```bash
python -m src.main
```

## Key Design Decisions 

- Uses `Decimal` for financial calculations (avoids floating point errors)
- `parse_decimal` detects whether the number uses comma or dot as decimal separator
- `TickerMapper` normalizes company names (strips "S.A.", "HOLDING", extra spaces) for fuzzy matching
- Tolerance for financial comparison is `0.01`
- Report statuses: `OK`, `ERRO_QUANTIDADE`, `ERRO_FINANCEIRO`, `FALTANTE_NO_BANCO`

