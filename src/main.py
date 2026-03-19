"""
Main execution entrypoint.
"""

from src.features.readers.internal_reader import read_internal_positions
from src.features.readers.custodian_reader import read_custodian_extract
from src.features.mapping.ticker_mapper import TickerMapper
from src.features.reconciliation.reconciler import reconcile
from src.features.writers.report_writer import write_report

def main():
    internal = read_internal_positions("src/data/input/internal_system.json")
    custodian = read_custodian_extract("src/data/input/custodian_extract.csv")
    mapper = TickerMapper()
    report = reconcile(internal, custodian, mapper)
    write_report(report, "src/data/output/relatorio_final.csv")

if __name__ == "__main__":
    main()