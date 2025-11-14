"""Results generation script for monolithic_2x2 model for Roberts 2020 FMICS paper."""

from pathlib import Path
from Tools import modest, sim_schema
from datetime import datetime
from pathvalidate import sanitize_filename
from typing import Literal, Tuple
from dataclasses import dataclass
from time import time

@dataclass
class Steps:
    low: int
    high: int
    stride: int

NoiseType = Literal["Resistive", "Inductive"]

def generate_model(original_model: str, clk: Steps, type: NoiseType):
    for i in range(clk.low, clk.high + 1, clk.stride):
        if type == "Resistive":
            original_model += f"\nproperty R_{i} = Pmax(<>[S(clk)<={i}] (resistiveNoise >= RESISTIVE_THRESH));"
        elif type == "Inductive":
            original_model += f"\nproperty R_{i} = Pmax(<>[S(clk)<={i}] (inductiveNoise >= INDUCTIVE_THRESH));"
    return original_model

def run_psn_analysis(
        max_clk: int,
        stride: int,
        batch: int,
        resistive_threshold: int,
        inductive_threshold: int,
        original_model: str
    ) -> Tuple[sim_schema.SimulationSummary, sim_schema.SimulationSummary]:
    """Runs psn analysis on the 2x2 model for `max_clk` cycles with a stride
    of `stride` cycles in batches of `batch`"""

    # Input validation
    assert 0 < max_clk
    assert 0 < stride and stride <= max_clk
    assert 0 < resistive_threshold
    assert 0 < inductive_threshold

    # constants for this analysis
    opts = ["--unsafe",
            "--max-run-length", "0", 
            "-D", 
            "--rng", "MersenneTwister", 
            "-E", f"RESISTIVE_THRESH={resistive_threshold}, INDUCTIVE_THRESH={inductive_threshold}"]

    # Create simulation data
    resistive_sims = sim_schema.SimulationSummary(
        title=f"resistive_monolithic_2x2",
        combined_data=[],
        sub_runs=[],
        total_time_sec=0.0,
        max_memory_mb=0.0
    )

    inductive_sims = sim_schema.SimulationSummary(
        title=f"inductive_monolithic_2x2",
        combined_data=[],
        sub_runs=[],
        total_time_sec=0.0,
        max_memory_mb=0.0
    )

    noc_parameters = sim_schema.NocParams(
        size=(2,2),
        buffer_size=4,
        activity_thresh=3,
        injection_rate_numerator=3,
        injection_rate_denominator=10,
        resistive_noise_threshold=resistive_threshold,
        inductive_noise_threshold=inductive_threshold
    )

    # Run resistive simulations
    for i in range(0, max_clk + 1, batch):
        low = i
        high = i + batch - 1
        if high >= max_clk: high = max_clk

        resistive_model = generate_model(original_model,
                                         Steps(low=low, high=high, stride=stride),
                                         "Resistive")
        
        start = time()
        resistive_results = modest.simulate(resistive_model, opts=opts)
        elapsed = time() - start

        this_run = sim_schema.SimulationRun(
            noc_parameters=noc_parameters.model_dump(),
            noc_model_file=resistive_model,
            modest_command=f"modest <model_file> {" ".join(opts)}",
            raw_modest_output=resistive_results,
            verification_time_sec=elapsed,
            verification_type="modes",
            clock_cycle_bounds=(low, high)
        )

        resistive_sims.sub_runs += [this_run]

    # Run inductive simulations
    for i in range(0, max_clk + 1, batch):
        low = i
        high = i + batch - 1
        if high >= max_clk: high = max_clk  
    
        inductive_model = generate_model(original_model,
                                         Steps(low=low, high=high, stride=stride),
                                         "Inductive")
        
        inductive_results = modest.simulate(inductive_model, opts=opts)

        this_run = sim_schema.SimulationRun(
            noc_parameters=noc_parameters.model_dump(),
            noc_model_file=inductive_model,
            modest_command=f"modest <model_file> {" ".join(opts)}",
            raw_modest_output=inductive_results,
            verification_time_sec=elapsed,
            verification_type="modes",
            clock_cycle_bounds=(low, high)
        )

        inductive_sims.sub_runs += [this_run]

    return (resistive_sims, inductive_sims)

def main():
    # Check if modest is available
    if not modest.is_modest_on_path():
        print("Modest executable not found. Exiting...")
        exit(1)
    
    # Locate the script directory
    script_dir = Path(__file__).resolve().parent

    # Setup the output directory
    output_dir = script_dir / sanitize_filename(f"results_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}")
    output_dir.mkdir()

    # Run the simulations
    with open(script_dir / "monolithic_2x2.modest", "r") as f:
        model = f.read()

    (r, i) = run_psn_analysis(10, 1, 10, 5, 5, model)

    # Save the output
    sim_schema.save_as_directory(r, output_dir)
    sim_schema.save_as_directory(i, output_dir)

if __name__ == "__main__":
    main()
else:
    print("Driver should only be run as a main CLI script.")
    exit(1)

