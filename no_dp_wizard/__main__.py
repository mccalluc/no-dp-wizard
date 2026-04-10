from pathlib import Path
from sys import argv
from no_dp_wizard import analyze_tsv

analysis = analyze_tsv(Path(argv[1]))
assert len(analysis) == 1
for k, v in analysis[0].items():
    print(f"{k}: {v}")
