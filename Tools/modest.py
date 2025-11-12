import shutil
import subprocess
import tempfile
from pathlib import Path

MODEST_EXECUTABLE: str = "modest"

def is_modest_on_path() -> bool:
    """Checks if 'modest' is available in the system's PATH.

    Returns:
        bool: True if 'modest' is found, False otherwise.
    """
    return shutil.which(MODEST_EXECUTABLE) is not None

def __run(model: str, command: list[str], *, opts: list[str] = []) -> str:
    """Runs the modest tool with the given model.

    Args:
        model (str): String repr of the model
        command: the modest executable command
        opts: cli opts to pass to modest
    
    Returns:
        Output of running command + opts result as string
    """
    output: str = ""
    with tempfile.TemporaryFile("w", encoding="utf-8") as modelfile:
        # Write the model to the tempfile
        modelfile.write(model)
        # Create the modest command
        process_command = command + [modelfile] + opts
        # Run the modest command
        result = subprocess.run(process_command, capture_output=True, text=True)
        # Combine stdout and stderr
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        output = stdout + stderr

    # Return the combined stdout and stderr    
    return output

def check(model: str, opts: list[str] = []) -> str:
    """Runs the modest mcsta model checking engine.

    Args:
        model (str): String repr of the model
        opts: cli opts to pass to modest
    
    Returns:
        Output of running command + opts result as string
    """
    return __run(model, command=[MODEST_EXECUTABLE, "mcsta"], opts=opts)

def simulate(model: str, opts: list[str] = []) -> str:
    """Runs the modest mcsta model checking engine.
    
    Args:
        model (str): String repr of the model
        opts: cli opts to pass to modest
    
    Returns:
        Output of running command + opts result as string
    """
    return __run(model, command=[MODEST_EXECUTABLE, "modes"], opts=opts)