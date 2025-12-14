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

pattern = r"^r(\d+)_[RI]_(\d+)$"
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

    # Set to use only default fonts
    plt.rcParams["pdf.use14corefonts"] = True
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['mathtext.fontset'] = 'stix'

    for dir in subdirs:
        if not (dir / "summary.json").exists():
            continue

        # Setup the output directory
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        output_dir = dir / sanitize_filename(f"plots_{timestamp}_of_{dir.name}")
        output_dir.mkdir()
        
        # Load the project description
        project = sim_schema.load_from_directory(dir)

        # Get the width and height of the current router
        width = project.sub_runs[0].noc_parameters["size"][0]
        height = project.sub_runs[0].noc_parameters["size"][1]

        # Merge all the properties for this run together
        properties: Dict[str, float] = {}
        for run in project.sub_runs:
            properties = properties | run.properties

        # Properties as stored as a {str |-> float}, but we need to extract
        # the router id `r` and the clock cycle `c` from them in order to
        # plot noise vs time per router
        clk_data: Dict[int, Dict[int, float]] = {}
        for k, v in properties.items():
            r, c = extract_indices(k)
            if r not in clk_data:
                clk_data[r] = {}
            clk_data[r][c] = v

        # We don't write the data because we won't use it.
        # We need to write the data, sorted by `r` first then sorted by
        # clock cycle to unique files that can be used by TikZ
        # for r in sorted(clk_data):
        #     with open(output_dir / f"router_{r}.txt", "w") as f:
        #         f.write(f"# Data for router {r}\n")
        #         for clk, prob in sorted(clk_data[r].items()):
        #             f.write(f"{clk} {prob}\n")
        
        ## Next we'll plot the noise vs. time graphs for each result

        for cycles in [1, 5, 10, 50, 100, 250, 500, 1000]:
            # To start we'll calculate the bounds for the plot. We know that 
            # since each property is a probability it's bounded [0,1], but it
            # may actually be bounded by a smaller value. We'll calculate that
            # value and round up to the nearest 0.1 to get a tight, but clean
            # plot
            highest_prob: float = max(val for inner_dict in clk_data.values() for val in list(inner_dict.values())[:(cycles+1)])
            highest_prob_rounded: float = math.ceil(highest_prob * 20.0) / 20.0

            ## Plot 1 - Noise vs. Cycles per Router (Small)
            # Now in a subplot we'll plot the noise vs. cycles plot for
            # each router
            if width <= 3 and height <= 3:
                fig = plt.figure(figsize=(3, 3))
                plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
                for r in sorted(clk_data):
                    plt.subplot(height,width,r+1)
                    x, y = zip(*sorted(clk_data[r].items()))
                    stop_index = next((i for i, val in enumerate(list(x)) if val >= cycles), None)
                    if stop_index is None:
                        stop_index = int(max(list(x)))
                    plt.plot(x[:(stop_index+1)], y[:(stop_index+1)], color='black')
                    plt.title(f"R{r}", fontsize=8)
                    plt.xticks(fontsize=6)
                    plt.yticks(fontsize=6)
                    plt.grid(True, color='lightgray', linestyle='--', linewidth=0.5, alpha=0.7)
                    ax = plt.gca()
                    for spine in ax.spines.values():
                        spine.set_color('darkgray')
                    plt.ylim(0.0, highest_prob_rounded)
                
                # fig.suptitle(f"$x \\in [0,{max(x)}]$, $y \\in [0,{highest_prob_rounded}]$")
                plt.tight_layout(pad=0.125)
                plt.savefig(output_dir / f"plot_small_{cycles}.pdf")
                plt.close('all')

            ## Plot 2 - Noise vs. Cycles per Router (Large)
            if width <= 4 and height <= 4:
                plt.figure(figsize=(6, 6))
                plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0.025, hspace=0.025)
                for r in sorted(clk_data):
                    plt.subplot(height,width,r+1)
                    x, y = zip(*sorted(clk_data[r].items()))
                    stop_index = next((i for i, val in enumerate(list(x)) if val >= cycles), None)
                    if stop_index is None:
                        stop_index = int(max(list(x)))
                    plt.plot(x[:(stop_index+1)], y[:(stop_index+1)], color='black')
                    plt.title(f"R{r}", fontsize=8)
                    plt.xticks(fontsize=6)
                    plt.yticks(fontsize=6)
                    plt.grid(True, color='lightgray', linestyle='--', linewidth=0.5, alpha=0.7)
                    ax = plt.gca()
                    for spine in ax.spines.values():
                        spine.set_color('darkgray')
                    plt.ylim(0.0, highest_prob_rounded)
                
                plt.tight_layout()
                plt.savefig(output_dir / f"plot_large_{cycles}.pdf")
                plt.close('all')

            ## Plot 3 - Heatmap
            # Create a heatmap where each cell represents the max probability for each router
            max_probs = [[0 for _ in range(width)] for _ in range(height)]
            for r in sorted(clk_data):
                row = r // width
                col = r % width
                max_probs[row][col] = max(list(clk_data[r].values())[:(cycles+1)])
            
            hmap_max = max(max(r) for r in max_probs)
            hmap_min = min(min(r) for r in max_probs)

            # Round
            hmap_max = math.ceil(hmap_max * 10) / 10
            hmap_min = math.floor(hmap_min * 10) / 10

            # Bound
            hmap_max = 1.0 if hmap_max > 1.0 else hmap_max
            hmap_min = 0.0 if hmap_min < 0.0 else hmap_min

            plt.figure(figsize=(6,6))
            plt.imshow(max_probs, cmap='YlGnBu', vmin=hmap_min, vmax=hmap_max, origin='upper')
            plt.colorbar(shrink=0.8)
            plt.xticks([])
            plt.yticks([])
            plt.tight_layout()
            plt.savefig(output_dir / f"heatmap_{cycles}.pdf", bbox_inches='tight')
            plt.close('all')

            ## Plot 4 - Heatmap Small
            # Create a heatmap where each cell represents the max probability for each router
            max_probs = [[0 for _ in range(width)] for _ in range(height)]
            for r in sorted(clk_data):
                row = r // width
                col = r % width
                max_probs[row][col] = max(list(clk_data[r].values())[:(cycles+1)])
            
            hmap_max = max(max(r) for r in max_probs)
            hmap_min = min(min(r) for r in max_probs)

            # Round
            hmap_max = math.ceil(hmap_max * 10) / 10
            hmap_min = math.floor(hmap_min * 10) / 10

            # Bound
            hmap_max = 1.0 if hmap_max > 1.0 else hmap_max
            hmap_min = 0.0 if hmap_min < 0.0 else hmap_min

            plt.figure(figsize=(2,2))
            plt.imshow(max_probs, cmap='YlGnBu', vmin=hmap_min, vmax=hmap_max, origin='upper')
            plt.colorbar(shrink=0.8)
            plt.xticks([])
            plt.yticks([])
            plt.tight_layout()
            plt.savefig(output_dir / f"heatmap_{cycles}_small.pdf", bbox_inches='tight')
            plt.close('all')
        
        # Clean up before next loop
        del project, properties, clk_data