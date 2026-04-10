"""
Test bed to explore what kind of summary data currators can use
"""

import csv
from pathlib import Path
import polars as pl

package_root = Path(__file__).parent
__version__ = (package_root / "VERSION").read_text().strip()


# Copy-paste from dp-wizard:
def convert_to_csv(tab_path: Path) -> Path:
    """
    Converts a .tsv or .tab file to .csv,
    adds the new file in the same directory as the original,
    and returns the new Path.
    """
    accepted = [".tsv", ".tab"]
    if tab_path.suffix not in accepted:
        raise Exception(f"Expected {' or '.join(accepted)}, not {tab_path}")
    csv_path = tab_path.parent / f"{tab_path.stem}.csv"
    csv_handle = csv_path.open(mode="w")
    with tab_path.open(newline="") as tab_delim:
        reader = csv.reader(tab_delim, dialect=csv.excel_tab)
        writer = csv.writer(csv_handle)
        for row in reader:
            writer.writerow(row)
    csv_handle.flush()
    return csv_path


def analyze_tsv(tsv_path: Path):
    csv_path = convert_to_csv(tsv_path)
    return pl.scan_csv(csv_path).agg(pl.col("int_1").quantile(0.1)).collect()
