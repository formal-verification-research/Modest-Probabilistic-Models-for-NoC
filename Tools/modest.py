import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Tuple
import re

MODEST_EXECUTABLE: str = "modest"

def is_modest_on_path() -> bool:
    """Checks if 'modest' is available in the system's PATH.

    Returns:
        bool: True if 'modest' is found, False otherwise.
    """
    return shutil.which(MODEST_EXECUTABLE) is not None

def __run(model: str, command: list[str], *, opts: list[str] = []) -> Tuple[str, Dict[str, float]]:
    """Runs the modest tool with the given model.

    Args:
        model (str): String repr of the model
        command: the modest executable command
        opts: cli opts to pass to modest
    
    Returns:
        Output of running command + opts result as string
    """
    output: str = ""
    properties: Dict[str, float] = {}
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_model_path = Path(temp_dir) / "__tmp__.modest"
        temp_properties_path = Path(temp_dir) / "__tmp__.txt"

        # Write the model to the tempfile
        with open(temp_model_path, "w", encoding="utf-8") as model_file:
            model_file.write(model)

        # Create the modest command
        process_command = command + [model_file.name] + opts + ["-O", str(temp_properties_path), "minimal"]

        # Run the modest command
        result = subprocess.run(process_command, capture_output=True, text=True)

        # Combine stdout and stderr
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        output = stdout + stderr

        # Now capture the properties
        with open(temp_properties_path, "r") as property_file:
            for line in property_file.readlines():
                prop = list(filter(None, re.split(r"[:\s]", line)))
                if len(prop) != 2: continue
                properties[str(prop[0]).replace('"','')] = float(prop[1])

    # Return the combined stdout and stderr    
    return (output, properties)

def check(model: str, opts: list[str] = []) -> Tuple[str, Dict[str, float]]:
    """Runs the modest mcsta model checking engine.

    Args:
        model (str): String repr of the model
        opts: cli opts to pass to modest
    
    Returns:
        Output of running command + opts result as string
    """
    return __run(model, command=[MODEST_EXECUTABLE, "mcsta"], opts=opts)

def simulate(model: str, opts: list[str] = []) -> Tuple[str, Dict[str, float]]:
    """Runs the modest mcsta model checking engine.
    
    Args:
        model (str): String repr of the model
        opts: cli opts to pass to modest
    
    Returns:
        Output of running command + opts result as string
    """
    return __run(model, command=[MODEST_EXECUTABLE, "modes"], opts=opts)

__all__ = ["check", "simulate", "is_modest_on_path"]