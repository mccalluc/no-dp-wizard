from pathlib import Path

from no_dp_wizard import analyze_tsv


def test_analyze_tsv():
    analyze_tsv(Path(__file__))