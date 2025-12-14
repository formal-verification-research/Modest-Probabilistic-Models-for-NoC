"""Results generation script for modular models for Boes 2023 master's thesis."""

from pathlib import Path
from Tools import modest, sim_schema, chunked_range
from datetime import datetime
from pathvalidate import sanitize_filename
from typing import Literal, Dict
from dataclasses import dataclass
from time import time

NoiseType = Literal["Resistive", "Inductive"]

def generate_model(
        original_model: str,
        clk: range,
        type: NoiseType,
        width: int,
        height: int) -> str:
    num_routers = width*height

    # Add router instances
    original_model += "\npar {\n:: Clock()"
    for i in range(0,num_routers):
        original_model += f"\n:: Router({i})"
    original_model += "\n}\n"

    # Add properties
    for i in clk:
        if type == "Resistive":
            original_model += f"\nproperty R_{i} = Pmax(<>[S(clk_indicator)<={i}] (c_res >= RESISTIVE_THRESH));"
        elif type == "Inductive":
            original_model += f"\nproperty I_{i} = Pmax(<>[S(clk_indicator)<={i}] (c_ind >= INDUCTIVE_THRESH));"
    return original_model

def run_psn_analysis(
        max_clk: int,
        stride: int,
        batch: int,
        activity_threshold: int,
        original_model: str,
        sim_type: NoiseType,
        width: int,
        height: int,
        experiments: str = ""
    ) -> sim_schema.SimulationSummary:
    """Runs psn analysis on the modular model for `max_clk` cycles with a stride
    of `stride` cycles in batches of `batch`"""

    # Input validation
    assert 0 < max_clk
    assert 0 < stride and stride <= max_clk
    assert 0 < activity_threshold
    assert 1 <= width
    assert 1 <= height
    assert 3 <= width + height # minimum size is 2x1 or 1x2

    # Set experiments string
    if experiments != "":
        experiments = f"ACTIVITY_THRESH={activity_threshold},NOC_MESH_WIDTH={width},NOC_MESH_HEIGHT={height},{experiments}"
    else:
        experiments = f"ACTIVITY_THRESH={activity_threshold},NOC_MESH_WIDTH={width},NOC_MESH_HEIGHT={height}"

    # constants for this analysis
    opts = ["--max-run-length", "0", 
            "-D",
            "--unsafe",
            "--rng", "MersenneTwister", 
            "-E", experiments]

    # Create the title
    title = f"{sim_type}_{width}x{height}_a{activity_threshold}"

    # Create simulation data
    sims = sim_schema.SimulationSummary(
        title=title,
        sub_runs=[],
        total_time_sec=0.0
    )

    # Set up the noc params
    noc_parameters = sim_schema.NocParams(
        size=(width,height),
        buffer_size=4,
        activity_thresh=activity_threshold,
        injection_rate_numerator=3,
        injection_rate_denominator=10
    )

    # Run resistive simulations
    for i in chunked_range.chunked_range(0, max_clk+1, stride, batch):

        model = generate_model(original_model,
                               i,
                               sim_type,
                               width,
                               height)
        
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

        if 1.0 in properties.values():
            break

    return sims

def normal():
    # Locate the script directory
    script_dir = Path(__file__).resolve().parent

    # Run the 2x2 model
    try:
        with open(script_dir / "modular_counters.modest", "r") as f:
            model = f.read()
    except:
        print("Failed to open model file 'modular_counters.modest'")
        return
    
    # Display output
    print("Running counters model...")
    
    # Setup the output directory
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_dir = script_dir / sanitize_filename(f"results_counters_{timestamp}")
    output_dir.mkdir()

    for width, height in zip([2, 3, 4, 8, 12], [2, 3, 4, 8, 12]):
        print(f"Running {width}x{height} model...")

        thresh = 3

        # Resistive Simulations
        for res, clk in [(1,200),(5,250),(10,400),(20,600)]:
            print(f"Running resistive noise for {clk} cycles with thresh == {res}...")
            experiments = f"RESISTIVE_THRESH={res},INDUCTIVE_THRESH=0"
            r = run_psn_analysis(max_clk=clk,
                                stride=1,
                                batch=100,
                                activity_threshold=thresh,
                                original_model=model,
                                sim_type="Resistive",
                                width=width,
                                height=height,
                                experiments=experiments)
            sim_schema.save_as_directory(r, output_dir)

        # Inductive 2x2 Simulations
        for ind, clk in [(1,1500),(5,2500),(10,3500)]:
            print(f"Running inductive noise for {clk} cycles with thresh == {ind}...")
            experiments = f"RESISTIVE_THRESH=0,INDUCTIVE_THRESH={ind}"
            i = run_psn_analysis(max_clk=clk,
                                stride=10,
                                batch=100,
                                activity_threshold=thresh,
                                original_model=model,
                                sim_type="Inductive",
                                width=width,
                                height=height,
                                experiments=experiments)
            sim_schema.save_as_directory(i, output_dir)

def main():
    # Check if modest is available
    if not modest.is_modest_on_path():
        print("Modest executable not found. Exiting...")
        return
    
    normal()

if __name__ == "__main__":
    main()
else:
    print("Driver should only be run as a main CLI script.")
    exit(1)
