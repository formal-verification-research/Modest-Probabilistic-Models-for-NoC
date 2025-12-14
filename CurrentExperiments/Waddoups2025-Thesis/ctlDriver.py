"""Results generation script for modular models for Boes 2023 master's thesis."""

from pathlib import Path
from Tools import modest, sim_schema, chunked_range
from datetime import datetime
from pathvalidate import sanitize_filename
from typing import Literal, Dict
from dataclasses import dataclass
from time import time

NoiseType = Literal["Resistive", "Inductive"]

def run_ctl_analysis(
        original_model: str
    ) -> sim_schema.SimulationSummary:
    """Runs psn analysis on the modular model for `max_clk` cycles with a stride
    of `stride` cycles in batches of `batch`"""

    # constants for this analysis
    opts = ["--unsafe",
            "--chainopt",
            "-D"]

    # Create the title
    title = f"2x2_ctl_check"

    # Create simulation data
    sims = sim_schema.SimulationSummary(
        title=title,
        sub_runs=[],
        total_time_sec=0.0
    )

    # Set up the noc params
    noc_parameters = sim_schema.NocParams(
        size=(2,2),
        buffer_size=4,
        activity_thresh=0,
        injection_rate_numerator=0,
        injection_rate_denominator=0
    )

    start = time()
    results, properties = modest.check(original_model, opts=opts)
    elapsed = time() - start

    opt_string = " ".join(opts)
    this_run = sim_schema.SimulationRun(
        noc_parameters=noc_parameters.model_dump(),
        noc_model_file=original_model,
        modest_command=f"modest <model_file> {opt_string}",
        raw_modest_output=results,
        verification_time_sec=elapsed,
        verification_type="mcsta-CTL",
        clock_cycle_bounds=(0,0),
        properties=properties
    )

    sims.sub_runs += [this_run]
    sims.total_time_sec += elapsed

    return sims

def ctl_nick():
    # Locate the script directory
    script_dir = Path(__file__).resolve().parent

    # Run the 2x2 model
    try:
        with open(script_dir / "modular_ctl.modest", "r") as f:
            model = f.read()
    except:
        print("Failed to open model file 'modular_ctl.modest'")
        return
    
    # Display output
    print("Running ctl checking ...")
    
    # Setup the output directory
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_dir = script_dir / sanitize_filename(f"results_ctl_{timestamp}")
    output_dir.mkdir()

    # Resistive 2x2 Simulations
    r = run_ctl_analysis(original_model=model)
    sim_schema.save_as_directory(r, output_dir)

def ctl_jonah():
    # Locate the script directory
    script_dir = Path(__file__).resolve().parent

    # Run the 2x2 model
    try:
        with open(script_dir / "modular_ctl_jonah.modest", "r") as f:
            model = f.read()
    except:
        print("Failed to open model file 'modular_ctl_jonah.modest'")
        return
    
    # Display output
    print("Running ctl checking (jonah) ...")
    
    # Setup the output directory
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_dir = script_dir / sanitize_filename(f"results_ctl_jonah_{timestamp}")
    output_dir.mkdir()

    # Resistive 2x2 Simulations
    r = run_ctl_analysis(original_model=model)
    sim_schema.save_as_directory(r, output_dir)

def main():
    # Check if modest is available
    if not modest.is_modest_on_path():
        print("Modest executable not found. Exiting...")
        return
    
    ctl_nick()

if __name__ == "__main__":
    main()
else:
    print("Driver should only be run as a main CLI script.")
    exit(1)
