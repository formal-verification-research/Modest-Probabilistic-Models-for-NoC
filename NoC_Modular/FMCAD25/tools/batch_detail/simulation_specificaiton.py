from pathlib import Path 

# Classes
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
        self.iter_vars: dict[int, tuple] = {}

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
        ret += f"Iteration variables:"
        for var, v_range in self.iter_vars.items():
            # capture var name
            with self.file.open() as f:
                lines = f.readlines()
            var_name = LINE_MATCH_RE.match(lines[var]).group(1)

            # get pretty range
            p_range = f"{v_range[0]} to {v_range[2]} (step size of {v_range[1]})"

            # put it all together to get the information
            ret += f"\n\t{var_name} in range {p_range} on line {var}"

        return ret

    def add_iter_var(self, line_num: int, iter_range: str) -> None:
        """Adds a variable to be iterated through during sequential simulation runs
        
        Required inputs:
        - line_num: the line number that the variable is found on in the self.model file
        - iter_range: the range which to iterate over in the format <start>[:<step>]:<end>"""
        # check if range is valid
        range_match = RANGE_MATCH_RE.match(iter_range)

        if range_match is None:
            print(f"Range argument {iter_range} is not in the correct format")
            print(f"\tin simspec {self.name}")
            print(f"")
            print(f"Correct format:")
            print(
                f"<start>:<step>:<end> | <start>:<end>\n\twhere the second option has an implied step of 1"
            )
            return None
        else:
            # check if the implied step is 1
            if range_match.group(3) == "":
                start_r = range_match.group(1)
                end_r = range_match.group(2)
                step_r = 1
            else:
                start_r = range_match.group(1)
                step_r = range_match.group(2)
                end_r = range_match.group(3)

            # convert the values to integers
            start_r = parse_int(start_r)
            step_r = parse_int(step_r)
            # add one step to the end because of 0-based indexing
            end_r = parse_int(end_r) + step_r

        # set the iteration variables in the simspec class
        self.iter_vars[line_num] = (start_r, step_r, end_r)

    def vars_to_list(self) -> List[tuple]:
        """Returns the vars to iterate over as list of tuples, in this format:
        [(<line num>, <start>, <step>, <end>), (<line num...<end>)...]"""

        ret: List[tuple] = []

        for line_num, iter_range in self.iter_vars.items():
            tup: tuple = (line_num,) + iter_range
            ret.append(tup)

        return ret