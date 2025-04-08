import shutil
import subprocess
from pathlib import Path


def is_modest_on_path() -> bool:
    """Checks if 'modest' is available in the system's PATH.

    Returns:
        bool: True if 'modest' is found, False otherwise.
    """
    return shutil.which("modest") is not None

def __run(model: str | Path, output_path: Path | None = None, command: list[str] = ["modest", "check"], opts: list[str] = []) -> str | None:
    """Runs the modest tool with the given model and property files.

    Args:
        model_path (str | Path): Path to the model file or string repr of the model.
        output_path (Path | None): Path to the output file. If None, the output is
            returned as a string.
    
    Returns:
        None if output_path is set, modest result as string otherwise
    
    Raises:
        FileNotFoundError: If 'modest' is not found in the system's PATH.
        TypeError if model is not a string or Path.
    """

    if not is_modest_on_path():
        raise FileNotFoundError("modest is not on the system's PATH.")

    tmp_model = False

    if isinstance(model, str):
        if Path(model).exists():
            filename = model
        else:
            filename = "__tmp_model__.modest"
            with open(filename, "w") as f:
                f.write(model)
            tmp_model = True
    elif isinstance(model, Path):
        filename = model 
    else:
        raise TypeError(f"model must be a string or Path. Instead got {type(model)}")

    process_command = command + [filename] + opts

    result = subprocess.run(process_command, capture_output=True, text=True)

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    output = stdout + stderr

    if tmp_model:
        Path(filename).unlink(missing_ok=False)
        
    if output_path is not None:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output)
        return None
    else:
        return output

def check(model: str | Path, output_path: Path | None = None) -> str | None:
    return __run(model, output_path, ["modest", "check"])

def simulate(model: str | Path, output_path: Path | None = None) -> str | None:
    return __run(model, output_path, command=["modest", "simulate"], opts=["--max-run-length", "0"])