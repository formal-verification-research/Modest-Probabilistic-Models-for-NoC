from pathlib import Path 
from enum import Enum

# Classes
class SimType(Enum):
    REWARD = 1
    NORMAL = 2

class SimVariable:
    """A variable that is set by the batcher during simulation."""

    def __init__(self, name: str, start: int, stop: int, step: int):
        """Creates a new simulation variable

        Required inputs:
        - name: The name of the variable
        - start: The starting value of the variable
        - stop: The stopping value of the variable
        - step: The step size of the variable"""

        self.name: str = name
        self.start: int = start
        self.stop: int = stop
        self.step: int = step
    
    def __str__(self) -> str:
        """Returns a string detailing the information about this simulation variable"""
        
        ret: str = f"{self.name} [{self.start}:{self.step}:{self.stop}]"

        return ret


class SimSpec:
    """The specification for a modest simulation"""

    def __init__(
        self,
        name: str,
        model: Path,
        output: Path,
        *,
        command: str = "simulate --max-run-length 0",
    ) -> None:
        """Creates a new simulation specification

        Required inputs:
        - name: The name of the specification
        - model: A file path to the .modest model
        - output: A file path to the output file

        Optional inputs
        - command: The command to run with modest. Do not include the model file name or the modest executable path."""

        self.name: str = name
        self.model: Path = model
        self.output: Path = output
        self.command: str = command
        self.type: SimType = SimType.NORMAL
        self.iter_vars: list[SimVariable] = {}

    def __str__(self) -> str:
        """Returns a string detailing the information about this simulation specification"""
        # Add simulation name
        ret: str = f"Simulation: {self.name}\n"

        # Add file name
        ret += f"Model: {self.model.name}\n"
        ret += f"Output: {self.output.name}\n"

        # Add simulation command
        ret += f"Command: modest {self.command} {self.file}\n"

        # Add iteration variables
        ret += f"Iteration variables:\n"
        for var in self.iter_vars:
            ret += f"  {var}\n"

        return ret