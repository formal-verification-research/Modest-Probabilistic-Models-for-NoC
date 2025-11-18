"""Results generation script for modular models for Boes 2023 master's thesis."""

from pathlib import Path
from Tools import modest, sim_schema, chunked_range
from datetime import datetime
from pathvalidate import sanitize_filename
from typing import Literal, Dict
from dataclasses import dataclass
from time import time

NoiseType = Literal["Resistive", "Inductive"]

def generate_model(original_model: str, clk: range, type: NoiseType):
    for router in range(0,9):
        for i in clk:
            if type == "Resistive":
                original_model += f"\nproperty r{router}_R_{i} = Pmax(<>[S(clk)<={i}] (noc[{router}].thisActivity >= ACTIVITY_THRESH));"
            elif type == "Inductive":
                original_model += f"\nproperty r{router}_I_{i} = Pmax(<>[S(clk)<={i}] (abs(noc[{router}].thisActivity - noc[{router}].lastActivity) >= ACTIVITY_THRESH));"
    return original_model

def run_psn_analysis(
        max_clk: int,
        stride: int,
        batch: int,
        activity_threshold: int,
        original_model: str,
        sim_type: NoiseType
    ) -> sim_schema.SimulationSummary:
    """Runs psn analysis on the modular model for `max_clk` cycles with a stride
    of `stride` cycles in batches of `batch`"""

    # Input validation
    assert 0 < max_clk
    assert 0 < stride and stride <= max_clk
    assert 0 < activity_threshold

    # constants for this analysis
    opts = ["--unsafe",
            "--max-run-length", "0", 
            "-D", 
            "--rng", "MersenneTwister", 
            "-E", f"ACTIVITY_THRESH={activity_threshold}"]

    # Create the title
    title = f"{sim_type}_new_prob_3x3_a{activity_threshold}"

    # Create simulation data
    sims = sim_schema.SimulationSummary(
        title=title,
        sub_runs=[],
        total_time_sec=0.0
    )

    # Set up the noc params
    noc_parameters = sim_schema.NocParams(
        size=(3,3),
        buffer_size=4,
        activity_thresh=activity_threshold,
        injection_rate_numerator=3,
        injection_rate_denominator=10
    )

    # Run resistive simulations
    for i in chunked_range.chunked_range(0, max_clk+1, stride, batch):

        model = generate_model(original_model,
                               i,
                               sim_type)
        
        start = time()
        results, properties = modest.simulate(model, opts=opts)
        elapsed = time() - start

        opt_string = " ".join(opts)
        this_run = sim_schema.SimulationRun(
            noc_parameters=noc_parameters.model_dump(),
            noc_model_file=model,
            modest_command=f"modest <model_file> {opt_string}",
            raw_modest_output=results,
            verification_time_sec=elapsed,
            verification_type="modes",
            clock_cycle_bounds=(min(i), max(i)),
            properties=properties
        )

        sims.sub_runs += [this_run]
        sims.total_time_sec += elapsed

    return sims

def main():
    # Check if modest is available
    if not modest.is_modest_on_path():
        print("Modest executable not found. Exiting...")
        exit(1)
    
    # Locate the script directory
    script_dir = Path(__file__).resolve().parent

    # Setup the output directory
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_dir = script_dir / sanitize_filename(f"results_{timestamp}")
    output_dir.mkdir()

    # Run the 2x2 model
    with open(script_dir / "modular_new_probabilities.modest", "r") as f:
        model = f.read()

    # Resistive 2x2 Simulations
    for thresh, clk in [(1,2000),(2,2000),(3,2000),(4,2000),(5,2000)]:
        r = run_psn_analysis(max_clk=clk,
                             stride=1,
                             batch=100,
                             activity_threshold=thresh,
                             original_model=model,
                             sim_type="Resistive")
        sim_schema.save_as_directory(r, output_dir)

    # Inductive 2x2 Simulations
    for thresh, clk in [(1,2000),(2,2000),(3,2000),(4,2000),(5,2000)]:
        i = run_psn_analysis(max_clk=clk,
                             stride=1,
                             batch=100,
                             activity_threshold=thresh,
                             original_model=model,
                             sim_type="Inductive")
        sim_schema.save_as_directory(i, output_dir)

if __name__ == "__main__":
    main()
else:
    print("Driver should only be run as a main CLI script.")
    exit(1)

