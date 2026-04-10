from pathlib import Path

from no_dp_wizard import analyze_tsv


def test_analyze_tsv():
    assert analyze_tsv(Path(__file__).parent / 'fake.tsv') == []