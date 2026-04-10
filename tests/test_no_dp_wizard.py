from pathlib import Path
import subprocess

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


def test_run_module():
    assert (
        subprocess.check_output(
            "python -m no_dp_wizard tests/fake.tsv".split(" "), text=True
        ).strip()
        == """
int_1_10_percent: 1
int_1_90_percent: 10
float_1_10_percent: 100
float_1_90_percent: 1000
""".strip()
    )
