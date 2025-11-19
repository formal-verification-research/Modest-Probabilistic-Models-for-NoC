import json
from pathlib import Path
from typing import List, Dict, Any, Literal, Optional, Tuple, Annotated, Union
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from pathvalidate import sanitize_filename
import os

class NocParams(BaseModel):
    """Stores all parameters for a modular NoC model"""
    model_config = ConfigDict(extra='allow')
    size: Tuple[int, int]
    buffer_size: int
    activity_thresh: int
    injection_rate_numerator: Optional[int]   = None
    injection_rate_denominator: Optional[int] = None
    resistive_noise_threshold: Optional[int]  = None
    inductive_noise_threshold: Optional[int]  = None

# This defines the possible verification types
VerificationType = Literal["mcsta-CTL", "mcsta-PMC", "modes"]

class SimulationRun(BaseModel):
    """Stores all data for a single Modest verification run."""
    model_config = ConfigDict(extra='allow')
    noc_parameters: Dict[str, Any]
    noc_model_file: str
    modest_command: str
    raw_modest_output: str
    verification_time_sec: float
    properties: Annotated[
        Dict[str, Union[float, bool]],
        Field(description="{Property name} -> {float (pctl) || bool (ctl)}")
    ] = {}
    verification_type: VerificationType
    clock_cycle_bounds: Tuple[int, int]
    # `new_field: Optional[str] = None`

class SimulationSummary(BaseModel):
    """Stores a summary of multiple related sub-runs."""
    model_config = ConfigDict(extra='allow')
    title: str
    sub_runs: Annotated[
        List[SimulationRun],
        Field(description="The full data for each sub-run")
    ]
    total_time_sec: float

def save_as_directory(summary: SimulationSummary, base_dir: Path) -> Path:
    """Saves the summary in a structured directory."""
    
    print(f"Saving summary of {summary.title}...")

    # 1. Create the main directory for the summary
    summary_dir_name = Path(sanitize_filename(summary.title))
    summary_dir = base_dir / summary_dir_name
    summary_dir.mkdir(parents=True, exist_ok=True)
    print(f" - saving summary to {summary_dir}")
    
    # 2. Save each sub-run in its own subdirectory
    sub_run_identifiers: List[str] = []
    for idx, run in enumerate(summary.sub_runs):
        # Use index-based directory name since title is no longer available
        run_dir_name = Path(sanitize_filename(f"run_{idx}"))
        run_dir = summary_dir / run_dir_name
        run_dir.mkdir(exist_ok=True)
        print(f" - saving run {idx} to {run_dir}")
        
        # 2a. Create a metadata dict for everything else
        metadata = run.model_dump(
            exclude={'noc_model_file', 'raw_modest_output'}
        )
        
        # 2b. Create the model and output filenames
        metadata["noc_model_file_path"] = "noc_model.modest"
        metadata["raw_modest_output_path"] = "modest_output.txt"

        # 2ac. Save the bulk text as separate files
        (run_dir / metadata["noc_model_file_path"]).write_text(run.noc_model_file, encoding='utf-8')
        (run_dir / metadata["raw_modest_output_path"]).write_text(run.raw_modest_output, encoding='utf-8')
        
        # 2d. Save the metadata as a JSON file
        with open(run_dir / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
            
        sub_run_identifiers.append(str(run_dir_name))

    # 3. Save the main summary file
    summary_metadata = summary.model_dump(exclude={'sub_runs'})
    
    # Store the names of the sub-run directories
    summary_metadata["sub_run_dirs"] = sub_run_identifiers
    
    # Dump the summary json out to file
    with open(summary_dir / "summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary_metadata, f, indent=2)
    
    print("...Done.")
    print("Directory structure:")

    # Directory structure printing
    def print_directory_tree(startpath):
        for root, dirs, files in os.walk(summary_dir):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 2 * (level)
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for f in files:
                print(f'{subindent}{f}')
    
    print_directory_tree(str(summary_dir.absolute()))

    # Return the path for the main summary dir
    return summary_dir

def load_from_directory(summary_dir: Path) -> SimulationSummary:
    """Loads a summary from a structured directory."""
    print(f"Loading from Directory: {summary_dir}")
    
    # 1. Load the main summary file
    with open(summary_dir / "summary.json", 'r', encoding='utf-8') as f:
        summary_data = json.load(f)

    # 2. Load each sub-run
    loaded_runs = []
    for run_dir_name in summary_data["sub_run_dirs"]:
        run_dir = summary_dir / run_dir_name
        
        # 2a. Load the metadata
        with open(run_dir / "metadata.json", 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # 2b. Load the bulk text files
        model_file = (run_dir / metadata["noc_model_file_path"]).read_text(encoding='utf-8')
        output_file = (run_dir / metadata["raw_modest_output_path"]).read_text(encoding='utf-8')
        
        # 2c. Remove the file path references before creating the object
        metadata.pop("noc_model_file_path", None)
        metadata.pop("raw_modest_output_path", None)
        
        # 2d. Create the SimulationRun object
        run_obj = SimulationRun.model_validate({
            **metadata,  # Unpack all metadata
            "noc_model_file": model_file,  # Add the full text
            "raw_modest_output": output_file # Add the full text
        })
        loaded_runs.append(run_obj)

    # 3. Create the final SimulationSummary object, excluding sub_run_dirs
    summary_data.pop("sub_run_dirs", None)
    return SimulationSummary.model_validate({
        **summary_data, # Unpack summary metadata
        "sub_runs": loaded_runs # Add the list of loaded run objects
    })

__all__ = ["NocParams",
           "VerificationType",
           "SimulationRun",
           "SimulationSummary", 
           "save_as_directory",
           "load_from_directory"]