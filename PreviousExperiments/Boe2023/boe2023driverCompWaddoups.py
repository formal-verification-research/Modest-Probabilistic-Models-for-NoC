"""Results generation script for modular models for Boes 2023 master's thesis."""

from pathlib import Path
from Tools import modest, sim_schema, chunked_range
from datetime import datetime
from pathvalidate import sanitize_filename
from typing import Literal, Dict
from dataclasses import dataclass
from time import time

@dataclass
class Steps:
    low: int
    high: int
    stride: int

NoiseType = Literal["Resistive", "Inductive"]
NoCSize = Literal["2x2", "3x3"]

def generate_model(original_model: str, clk: range, type: NoiseType):
    for i in clk:
        if type == "Resistive":
            original_model += f"\nproperty R_{i} = Pmax(<>[S(clk)<={i}] (resistiveNoise >= RESISTIVE_NOISE_THRESH));"
        elif type == "Inductive":
            original_model += f"\nproperty I_{i} = Pmax(<>[S(clk)<={i}] (inductiveNoise >= INDUCTIVE_NOISE_THRESH));"
    return original_model

def run_psn_analysis(
        max_clk: int,
        stride: int,
        batch: int,
        resistive_threshold: int,
        inductive_threshold: int,
        original_model: str,
        sim_type: NoiseType,
        size: NoCSize
    ) -> sim_schema.SimulationSummary:
    """Runs psn analysis on the modular model for `max_clk` cycles with a stride
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
            "-E", f"RESISTIVE_NOISE_THRESH={resistive_threshold}, INDUCTIVE_NOISE_THRESH={inductive_threshold}"]

    # Create the title
    title = f"{sim_type}_modular_{size}_" + (f"r{resistive_threshold}" if sim_type == "Resistive" else f"i{inductive_threshold}")

    # Create simulation data
    sims = sim_schema.SimulationSummary(
        title=title,
        sub_runs=[],
        total_time_sec=0.0
    )

    # Set up the noc params
    noc_parameters = sim_schema.NocParams(
        size=(2,2) if size == "2x2" else (3,3),
        buffer_size=4,
        activity_thresh=3,
        injection_rate_numerator=3,
        injection_rate_denominator=10,
        resistive_noise_threshold=resistive_threshold,
        inductive_noise_threshold=inductive_threshold
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
    output_dir = script_dir / sanitize_filename(f"results_comp_waddoups_{timestamp}")
    output_dir.mkdir()

    # Run the 2x2 model
    with open(script_dir / "modular_2x2.modest", "r") as f:
        model = f.read()

    # Resistive 2x2 Simulations
    thresh = 5
    clk = 100
    r = run_psn_analysis(max_clk=clk,
                            stride=1,
                            batch=250,
                            resistive_threshold=thresh,
                            inductive_threshold=1,
                            original_model=model,
                            sim_type="Resistive",
                            size="2x2")
    sim_schema.save_as_directory(r, output_dir)

if __name__ == "__main__":
    main()
else:
    print("Driver should only be run as a main CLI script.")
    exit(1)

