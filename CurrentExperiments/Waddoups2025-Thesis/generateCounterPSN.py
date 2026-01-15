from pathlib import Path
from pathvalidate import sanitize_filename
from datetime import datetime
import sys
import os
from Tools import sim_schema
from typing import Dict, Tuple
import re
import matplotlib.pyplot as plt
import math

pattern = r"^[RI]_(\d+)$"
matcher = re.compile(pattern)

def extract_indices(prop_label: str) -> int:
    match = matcher.match(prop_label)

    i = int(match.group(1))
    
    return i

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
    elif "counters" not in results_dir.name:
        print(f"This plotting script only works on ``counters'' output.")
        exit(1)
    else:
        results_dir = results_dir.resolve()

    # Set to use only default fonts
    plt.rcParams["pdf.use14corefonts"] = True
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['mathtext.fontset'] = 'stix'

    for noise_type in ["Resistive", "Inductive"]:
        for size in [2, 3, 4, 8, 12]:
            size_s = f"{size}x{size}"
            subdirs = [Path(f.path).resolve() 
                       for f in os.scandir(results_dir) 
                       if f.is_dir() and size_s in f.name and noise_type in f.name]

            # Setup the output directory
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            output_dir = results_dir / sanitize_filename(f"plots_{timestamp}_{noise_type}_{size}x{size}")
            output_dir.mkdir(exist_ok=True)

            data = []
            for dir in subdirs:
                if not (dir / "summary.json").exists():
                    continue
                
                # Load the project description
                project = sim_schema.load_from_directory(dir)

                # Get the width and height of the current router
                width = project.sub_runs[0].noc_parameters["size"][0]
                height = project.sub_runs[0].noc_parameters["size"][1]

                assert width == size
                assert height == size

                # Get the current threshold
                if noise_type == "Resistive":
                    thresh = int(project.sub_runs[0].noc_parameters["resistive_noise_threshold"])
                elif noise_type == "Inductive":
                    thresh = int(project.sub_runs[0].noc_parameters["inductive_noise_threshold"])
                else:
                    thresh = None
                
                assert isinstance(thresh, int)

                # Merge all the properties for this run together
                properties: Dict[str, float] = {}
                for run in project.sub_runs:
                    properties = properties | run.properties
                
                numeric_props: Dict[int, float] = {}
                for k, v in properties.items():
                    clk = extract_indices(k)
                    prob = float(v)
                    assert isinstance(clk, int)
                    assert isinstance(prob, float)
                    numeric_props[clk] = prob
                
                # Prepare data for plotting
                x, y = zip(*sorted(numeric_props.items()))
                data.append((thresh, x, y))
            
            # Create Figure
            if data:
                fig, ax = plt.subplots(figsize=(6, 6))
                for thresh, x, y in sorted(data, key=lambda t: t[0]):
                    ax.plot(x, y, label=f"$\\ge$ {thresh}")
                ax.legend()
                ax.set_xlabel("Clock Cycles")
                ax.set_ylabel("Probability")
                plt.savefig(output_dir / f"{noise_type}_{size}x{size}_counters.pdf", bbox_inches='tight')
                plt.close()

                fig, ax = plt.subplots(figsize=(3, 3))
                for thresh, x, y in sorted(data, key=lambda t: t[0]):
                    ax.plot(x, y, label=f"$\\ge$ {thresh}")
                ax.legend()
                ax.set_xlabel("Clock Cycles")
                ax.set_ylabel("Probability")
                plt.savefig(output_dir / f"{noise_type}_{size}x{size}_counters_small.pdf", bbox_inches='tight')
                plt.close()