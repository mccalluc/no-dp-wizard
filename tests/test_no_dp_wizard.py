from pathlib import Path

from no_dp_wizard import analyze_tsv


def test_analyze_tsv():
    assert analyze_tsv(Path(__file__).parent / "fake.tsv") == [
        {
            "float_1_10_percent": 100,
            "float_1_90_percent": 1000,
            "int_1_10_percent": 1,
            "int_1_90_percent": 10,
        },
    ]
