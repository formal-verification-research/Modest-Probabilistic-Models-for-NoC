from pathlib import Path
from pathvalidate import sanitize_filename
from datetime import datetime
import sys
import os
from Tools import sim_schema
from typing import Dict, Tuple
import re

pattern = r"^r(\d+)_R_(\d+)$"
matcher = re.compile(pattern)

def extract_indices(prop_label: str) -> Tuple[int, int]:
    # We add parentheses () around \d+ to create "capture groups".
    # Group 1 will be I, Group 2 will be J.
    match = matcher.match(prop_label)

    i = int(match.group(1))
    j = int(match.group(2))
    
    return i, j

if __name__ == "__main__":
    # Check inputs
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path to results dir>")
        exit(1)
    
    # Locate the script directory
    script_dir = Path(__file__).resolve().parent

    # Get the output directory
    results_dir = Path(sys.argv[1])
    if not results_dir.exists():
        print(f"Output directory supplied, ``{sys.argv[1]}'', was not found.")
        exit(1)
    else:
        results_dir = results_dir.resolve()

    # For each child directory, generate plot files (to go in latex)
    subdirs = [Path(f.path).resolve() for f in os.scandir(results_dir) if f.is_dir()]

    for dir in subdirs:
        if not (dir / "summary.json").exists():
            continue

        # Setup the output directory
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        output_dir = dir / sanitize_filename(f"plots_{timestamp}_of_{dir.name}")
        output_dir.mkdir()
        
        project = sim_schema.load_from_directory(dir)

        properties: Dict[str, float] = {}
        for run in project.sub_runs:
            properties = properties | run.properties

        clk_data: Dict[int, Dict[int, float]] = {}

        for k, v in properties.items():
            r, c = extract_indices(k)
            if r not in clk_data:
                clk_data[r] = {}
            clk_data[r][c] = v

        for r in sorted(clk_data):
            with open(output_dir / f"router_{r}.txt", "w") as f:
                f.write(f"# Data for router {r}\n")
                for clk, prob in sorted(clk_data[r].items()):
                    f.write(f"{clk} {prob}\n")