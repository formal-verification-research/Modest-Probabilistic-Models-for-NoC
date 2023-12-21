# Author: Nick Waddoups

import argparse
import os
from pprint import pprint
import shutil
import sys
import time
from typing import Dict, List
import tomlkit
import re
from pathlib import Path
from colorama import Fore, Style
from subprocess import Popen, PIPE, DEVNULL
from itertools import product
import pandas as pd

from tqdm import tqdm

# Global variables
verbose: bool = False

LINE_MATCH_RE = re.compile(r"\s*const\s+int\s+([_A-za-z0-9\-]+)[\s=0-9]*;\s*")
RANGE_MATCH_RE = re.compile(r"^(\d+):(\d+):?(\d*)")
MODEST_PROPERTY_NAME_RE = re.compile(r"\s*\+\s+Property\s+([A-Za-z_\-]+)\s*")
MODEST_PROBABILITY_RE = re.compile(r"\s+Estimated\s+probability:\s+([0-9\.]+)\s+")


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
        self.name: str = name
        self.model: Path = model
        self.output: Path = output
        self.command: str = command
        self.iter_vars: Dict[int, tuple] = {}

    def __str__(self) -> str:
        """Returns information about this simulation specification"""
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
        """Adds a variable to be iterated through during sequential simulation runs"""
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

            start_r = parse_int(start_r)
            step_r = parse_int(step_r)
            end_r = parse_int(end_r) + step_r

        self.iter_vars[line_num] = (start_r, step_r, end_r)

    def vars_to_list(self) -> List[tuple]:
        """Returns the vars to iterate over as list of tuples, in this format:
        [(<line num>, <start>, <step>, <end>), (<line num...<end>)...]"""

        ret: List[tuple] = []

        for line_num, iter_range in self.iter_vars.items():
            tup: tuple = (line_num,) + iter_range
            ret.append(tup)

        return ret


# Functions
def printv(*values: object, sep: str | None = " ", end: str | None = "\n") -> None:
    if verbose:
        print(f"{Fore.CYAN}(v){Style.RESET_ALL} ", end="")
        print(*values, sep=sep, end=end)


def parse_int(n: str | int) -> int | None:
    try:
        return int(n)
    except:
        return None


def permute_ranges(*args) -> (List[tuple], int):
    """Permutes n ranges into a tagged list of ranges"""
    ranges: List[tuple] = []
    num_ranges: int = 1

    for name, start, step, end in args:
        var_range = range(start, end, step)
        num_ranges *= len(var_range)
        ranges.append(var_range)
        ranges[-1] = [(name, n) for n in ranges[-1]]

    return (product(*ranges), num_ranges)


def get_parser():
    """This returns the argument parser for this script"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "specfile", help="MODEST simulation specification file", type=str
    )
    parser.add_argument(
        "--verbose", help="turn verbose comments on", action="store_true"
    )
    return parser


def check_specfile_path(specfile: str) -> Path | None:
    """Checks if the specfile is a real toml file"""
    # convert it to a path object
    specfile = Path(specfile)

    # check if it exists
    if not specfile.exists():
        print(f"Could not find simulation specification file at")
        print(f"{specfile}")
        print()
        print(f"Use --help for information on running this script")
        return None

    # check if it's a toml file
    if not specfile.suffix.lower() == ".toml":
        print(f"Simulation specification file {specfile} is not ", end="")
        print(f"a .toml file")
        print()
        print(f"Use --help for information on running this script")
        return None

    return specfile


def get_specs(path: Path) -> List[SimSpec] | None:
    """Checks if the contents of the spec file are valid"""
    printv(f"Reading .toml file {path} as string")
    with path.open() as f:
        specfile_as_str: str = f.read()

    printv(f"Parsing .toml file {path} using tomlkit")
    specfile: dict = tomlkit.parse(specfile_as_str).unwrap()

    specs: List[SimSpec] = []

    printv(f"Parsing simulation specifications in {path}")
    for spec in specfile:
        printv(
            f'Found simulation specification {Fore.GREEN}"{spec}"{Style.RESET_ALL}, variables found:'
        )

        # intially set model_file to None, this is how we check if there was a file arg or not
        model_file: Path | None = None
        output_file: Path | None = None

        # initially set command to None to check if a command was given or not
        command: str | None = None

        # iterate over all of the details looking for a modest file
        for var, val in specfile[spec].items():
            printv(f"\t{var} = {val}")

            # check if this is a file argument
            if var == "_model_" and model_file is None:
                # check if it's a valid file
                model_file = Path(val)
                if not model_file.exists():
                    print(
                        f"{Fore.RED}Error:{Style.RESET_ALL} Model file {val} does not exist."
                    )
                    print(f"\tTo fix update the filepath for {spec} in {path.name}.")
                    return None

                if not model_file.suffix == ".modest":
                    print(
                        f"{Fore.RED}Error:{Style.RESET_ALL} Model file {val} is not a Modest file."
                    )
                    print(
                        f"\tTo fix update the filepath for {spec} in {path.name} to include a modest file."
                    )
                    return None

            # get the output file
            if var == "_output_" and output_file is None:
                output_file = Path(val)
                if not (output_file.suffix == ".csv" or output_file.suffix == ".txt"):
                    print(
                        f"{Fore.RED}Error:{Style.RESET_ALL} Output file {val} is not a .txt or .csv file."
                    )
                    print(
                        f"\tTo fix update the filepath for {spec} in {path.name} to include a .txt or .csv file."
                    )
                    return None

            # check if this is a command argument
            if var == "_command_" and command is None:
                print(
                    f"{Fore.RED}Currently setting custom commands is not implemented.{Style.RESET_ALL}"
                )
                command = val

        # after iterating over the details check if a model was passed in
        if model_file is None:
            print(
                f"{Fore.RED}Error:{Style.RESET_ALL} Spec {spec} does not contain a '_model_' member."
            )
            print(f'\tTo fix add \'_model_ = "<path to modest file>" to {path.name}')
            return None
        else:
            specfile[spec].pop("_model_")

        # after iterating over the details check if a output file was passed in
        if output_file is None:
            print(
                f"{Fore.RED}Error:{Style.RESET_ALL} Spec {spec} does not contain a '_output_' member."
            )
            print(
                f'\tTo fix add \'_output_ = "<path to output file><.csv | .txt>" to {path.name}'
            )
            return None
        else:
            specfile[spec].pop("_output_")

        # check if we have a command or not
        if not command is None:
            specfile[spec].pop("_command_")

        # Then check if all of the requested iteration variables are in the modest file
        printv(f"Looking for requested iteration variables in {path}")
        with model_file.open() as f:
            lines = f.readlines()

        line_nums: Dict[str, int] = {}

        for index, line in enumerate(lines):
            for var in specfile[spec]:
                if var in line and not var in line_nums:
                    # check to make sure the line has correct syntax
                    if LINE_MATCH_RE.match(line) is None:
                        print(
                            f"{Fore.RED}Error:{Style.RESET_ALL} Line {index + 1} in {model_file.name} is not in the correct format:"
                        )
                        print(f"\t{line.strip()}")
                        print(f"\tFormat should be:")
                        print(f"\tonst int <var>[= <default>];")
                        print(f'\twhere "= <default>" is optional')

                    printv(
                        f"\tFound {Fore.YELLOW}{var}{Style.RESET_ALL} on line {index + 1}: {line.rstrip()}"
                    )

                    line_nums[var] = index
                    break

        _spec = SimSpec(spec, model_file, output_file)
        for var, val in specfile[spec].items():
            _spec.add_iter_var(line_nums[var], val)

        specs.append(_spec)
    return specs


def run_simulation(
    spec: SimSpec, *, tmp_file: Path = Path("./_tmp_model_.modest")
) -> pd.DataFrame | None:
    """Runs the simulation specified"""

    printv(f"{Fore.GREEN}Starting simulation for {spec.name}{Style.RESET_ALL}")

    printv(f"Opening {spec.model.name}")
    with spec.model.open("r") as f:
        model_lines = f.readlines()

    var_permutation = None
    len_range: int = 0

    (var_permutation, len_range) = permute_ranges(*(spec.vars_to_list()))

    if verbose:
        printv(f"Verbose mode is enabled, disabling tqdm status bar")
    else:
        var_permutation = tqdm(var_permutation, desc=f"{spec.name}", total=len_range)

    if var_permutation is None:
        print(
            f"{Fore.RED}ERROR:{Style.RESET_ALL} Variable permutation failed for {spec.name}"
        )
        return None

    # create the pandas dataframe to hold all the needed information
    sim_data: pd.DataFrame | None = None

    for range_vars in var_permutation:
        printv(f"Simulating permuation: {range_vars}")

        # create a temporary DataFrame to store this iterations data
        single_iter_data = {}

        # create a tracker to track if all probabilities are 1
        prob_tracker: float = 1.0

        # Extract all the const variable information
        for var in range_vars:
            # extract the line number
            line_num = var[0]
            # extract the variables value
            value = var[1]

            # find the variable on the line number
            line_match = LINE_MATCH_RE.match(model_lines[line_num])

            # check if there was actually a match
            if line_match is None:
                print(
                    f"{Fore.RED}ERROR:{Style.RESET_ALL} Failed to find a const variable on line {line_num + 1} of {spec.model.name} while simulating {spec.name}"
                )
                return None

            # get the variable name
            var_name = line_match.group(1)

            # update the line to have the new value
            new_line = f"const int {var_name} = {value};\n"

            # stick the new line in the file
            model_lines[line_num] = new_line
            printv(
                f'Added "{new_line.rstrip()}" to line {line_num} for {spec.name} simulation'
            )

            # add it to the single loop data
            single_iter_data[var_name] = value

        # Once the iteration variables are updated write the new modest model file
        printv(f"Opening temporary model file for writing {tmp_file}")
        with tmp_file.open("w") as f:
            f.writelines(model_lines)

        # now run the simulation through modest
        # get the command
        command = ["modest", *(spec.command.split()), str(tmp_file.absolute())]

        # open the process
        printv(f"Running simulation with command {command}")
        process = Popen(
            command,
            stdout=PIPE,
            stderr=PIPE,
        )

        # get output from process, out is stdout, err is stderr
        (out, err) = process.communicate()

        # split the output into individual lines
        out = out.decode("utf-8", "ignore").split("\r\n")
        printv(f"Modest output:{Style.DIM}\n{"\n".join(out).rstrip()}{Style.RESET_ALL}")
        printv(f"Finished simulation, finding properties")

        prob = None
        prop = None

        for line in out:
            prop_name = MODEST_PROPERTY_NAME_RE.match(line)
            prob_val = MODEST_PROBABILITY_RE.match(line)

            if not prop_name is None:
                prop = prop_name.group(1)

            if not prob_val is None:
                prob = prob_val.group(1)

            if not (prop is None or prob is None):
                printv(f"\tFound {prop} = {prob}")
                single_iter_data[prop] = prob

                prob_tracker *= float(prob)

                prop = None
                prob = None

        single_iter_df = pd.DataFrame(single_iter_data, index=[1])

        if sim_data is None:
            sim_data = single_iter_df
        else:
            sim_data = pd.concat([sim_data, single_iter_df])

        if prob_tracker >= 1.0:
            printv(f"All probabilities are 1, ending simualtion for {spec.name}")
            break

    printv(f"Removing temporary file {tmp_file}")
    if tmp_file.exists():
        os.remove(tmp_file)

    printv(f"Writing simulation data to {spec.output}")
    sim_data.to_csv(spec.output, index=False)

    return sim_data


if __name__ == "__main__":
    # Define the argument parser
    args = get_parser().parse_args()

    print(f"{Fore.YELLOW}--- MODEST Simulation Runner ---{Style.RESET_ALL}")

    # check if verbose mode is enabled
    if args.verbose:
        verbose = True
        print(f"{Fore.CYAN}--- Verbose mode enabled ---{Style.RESET_ALL}")
        print(
            f"All verbose outputs will be annotated with a {Fore.CYAN}(v){Style.RESET_ALL}"
        )
        print()

    # check if modest is installed
    if shutil.which("modest") is None:
        print(f"{Fore.RED}ERROR:{Style.RESET_ALL} could not find modest installation. Please add modest to the path")

    # check the spec file
    specfile_path = check_specfile_path(args.specfile)
    if specfile_path is None:
        print(
            f"{Fore.RED}Simulation specification .toml file is not valid. Looked for file at:{Style.RESET_ALL}"
        )
        print(f"{args.specfile}")
        sys.exit()

    # parse the spec file
    specs = get_specs(specfile_path)
    if specs is None:
        print(
            f"{Fore.RED}Simulation specifications could not be parsed{Style.RESET_ALL}"
        )
        sys.exit()

    # run the simulations
    print()
    print(f"{Fore.YELLOW}--- Starting Simulations ---{Style.RESET_ALL}")

    for spec in specs:
        print(run_simulation(spec))
        break

    print(f"{Fore.YELLOW}--- Finished Simulations ---{Style.RESET_ALL}")

else:
    sys.exit("This is not a module to be imported!")
