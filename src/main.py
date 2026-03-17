"""
Main execution entrypoint.
"""

from readers.internal_reader import read_internal_positions
from readers.custodian_reader import read_custodian_extract
from mapping.ticker_mapper import TickerMapper
from reconciliation.reconciler import reconcile
from writers.report_writer import write_report

def main():
    internal = read_internal_positions("internal_system.json")
    custodian = read_custodian_extract("custodian_extract.csv")
    mapper = TickerMapper()
    report = reconcile(internal, custodian, mapper)
    write_report(report, "relatorio_final.csv")

if __name__ == "__main__":
    main()