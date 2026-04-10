"""
Test bed to explore what kind of summary data currators can use
"""

import csv
from pathlib import Path
import polars as pl
import re
from math import log
from sys import argv

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


def percentile_expr(col, percentile):
    floor_or_ceil = "floor" if percentile < 50 else "ceil"
    log_expr = pl.col(col).quantile(percentile / 100).log10()
    exp_expr = getattr(log_expr, floor_or_ceil)().mul(log(10)).exp()
    return exp_expr.round().cast(pl.Int32).alias(f"{col}_{percentile}_percent")


def analyze_tsv(tsv_path: Path):
    csv_path = convert_to_csv(tsv_path)
    lf = pl.scan_csv(csv_path)
    all_numeric = [k for k, v in lf.collect_schema().items() if v.is_numeric()]
    first_numeric = []
    stems = set()
    for col in all_numeric:
        stem = re.sub(r"[^a-zA-Z]*\d+", "", col)
        if stem not in stems:
            first_numeric.append(col)
            stems.add(stem)
    pairs = [
        [percentile_expr(col, 10), percentile_expr(col, 90)] for col in first_numeric
    ]
    exprs = [expr for pair in pairs for expr in pair]
    return lf.select(*exprs).collect().to_dicts()


def wizard():
    analysis = analyze_tsv(Path(argv[1]))
    assert len(analysis) == 1
    for k, v in analysis[0].items():
        print(f"{k}: {v}")
