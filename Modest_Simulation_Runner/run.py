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

SCRIPT_VERSION: str = "1.0.0"
SCRIPT_AUTHOR: str = "Nick Waddoups"
SCRIPT_AUTHOR_EMAIL: str = "nick.waddoups@usu.edu"

LINE_MATCH_RE = re.compile(r"\s*const\s+int\s+([_A-za-z0-9\-]+)[\s=0-9]*;\s*")
RANGE_MATCH_RE = re.compile(r"^(\d+):(\d+):?(\d*)")
MODEST_PROPERTY_NAME_RE = re.compile(r"\s*\+\s+Property\s+([A-Za-z_\-]+)\s*")
MODEST_PROBABILITY_RE = re.compile(r"\s+Estimated\s+probability:\s+([0-9\.]+)\s+")

ERR = f"{Fore.RED}ERROR:{Style.RESET_ALL}"

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
        self.iter_vars: Dict[int, tuple] = {}

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


# Functions
def printv(*values: object, sep: str | None = " ", end: str | None = "\n") -> None:
    """Verbose wrapper around print. Adds (v) signifier and prints whatever is entered"""
    if verbose:
        print(f"{Fore.CYAN}(v){Style.RESET_ALL} ", end="")
        print(*values, sep=sep, end=end)


def parse_int(n: str | int) -> int | None:
    """Integer parser that doesn't throw an exception"""
    try:
        return int(n)
    except:
        return None


def permute_ranges(*args) -> (product, int):
    """Permutes n ranges into a tagged cartesion product of ranges
    
    Inputs:
    - args: each arg should be a tuple in the form of (<line number>, <start>, <step>, <stop>)

    Returns:
    - product: an iterator to each of values of the cartesian product
    - int: the total size of the iterator. itertools.product does not calculate this, so I do instead
        so that we can have progess bars
    
    Example:
    ```
    range_a = (37, 1, 1, 3)
    range_b = (45, 2, 2, 5)

    (p, n) = permute_ranges(range_a, range_b)
    # list(p) == [((37,1), (45,2),
    #              (37,1), (45,4),
    #              (37,2), (45,2),
    #              (37,2), (45,4))]
    # n == 4
    ```
    Here is how `list(p)[0]` would be intrepreted:
    
    list(p)[0] == ((37,1), (45,2))

    For simulation iteration 0, the const integer on line 37 of the modest model file
    will be set to 1, and the const integer on line 45 of the modest model file will be
    set to 2."""
    ranges: List[tuple] = []
    num_ranges: int = 1

    for line_num, start, step, end in args:
        # get the range of the value
        var_range = range(start, end, step)
        
        # calculate the number of ranges by doing a Reduction Multiplication over
        # all of the lengths of the ranges. Symbollically, this would look like
        # this:
        #   n_ranges = PI from 0 to n of len(range[n])
        # where PI is the reduction multiplication operator
        num_ranges *= len(var_range)
        ranges.append(var_range)

        # Tag the range with the line number
        ranges[-1] = [(line_num, n) for n in ranges[-1]]

    # product is the cartesian product defined in itertools
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
        print(f"{ERR} Could not find simulation specification file at")
        print(f"{specfile}")
        return None

    # check if it's a toml file
    if not specfile.suffix.lower() == ".toml":
        print(f"{ERR} Simulation specification file {specfile} is not ", end="")
        print(f"a .toml file")
        return None

    return specfile


def get_specs(path: Path) -> List[SimSpec] | None:
    """Checks if the contents of the spec file are valid and returns a list of specs
    
    Inputs:
    - path: path to the spec .toml file
    
    Outputs:
    - List[SimSpec] | None: List of specs if .toml is valid, None otherwise"""

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

            # check if this is a model file variable
            if var == "_model_" and model_file is None:
                # check if it's a valid file
                model_file = Path(val)
                if not model_file.exists():
                    print(
                        f"{ERR} Model file {val} does not exist."
                    )
                    print(f"\tTo fix update the filepath for {spec} in {path.name}.")
                    return None

                if not model_file.suffix == ".modest":
                    print(
                        f"{ERR} Model file {val} is not a Modest file."
                    )
                    print(
                        f"\tTo fix update the filepath for {spec} in {path.name} to include a modest file."
                    )
                    return None

            # check if this is an output file variable
            if var == "_output_" and output_file is None:
                output_file = Path(val)
                if not (output_file.suffix == ".csv" or output_file.suffix == ".txt"):
                    print(
                        f"{ERR} Output file {val} is not a .txt or .csv file."
                    )
                    print(
                        f"\tTo fix update the filepath for {spec} in {path.name} to include a .txt or .csv file."
                    )
                    return None

            # check if this is a command variable
            if var == "_command_" and command is None:
                printv(f"Found command variable for {spec} in {path.name}:")
                printv(f"\t_command_ = {val}")
                printv(f"Please note that commands are not checked for validity and may cause unexpected errors")
                command = val

        # after iterating over the details check if a model was passed in
        if model_file is None:
            print(
                f"{ERR} Spec {spec} does not contain a '_model_' member."
            )
            print(f'\tTo fix add \'_model_ = "<path to modest file>" to {path.name}')
            return None
        else:
            # remove it from the list so we only have iteration variables left
            specfile[spec].pop("_model_")

        # after iterating over the details check if a output file was passed in
        if output_file is None:
            print(
                f"{ERR} Spec {spec} does not contain a '_output_' member."
            )
            print(
                f'\tTo fix add \'_output_ = "<path to output file><.csv | .txt>" to {path.name}'
            )
            return None
        else:
            # remove it from the list so we only have iteration variables left
            specfile[spec].pop("_output_")

        # check if we have a command or not
        if command is None:
            command = "simulate --max-run-length 0"
        else:
            # remove it from the list so we only have iteration variables left
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
                            f"{ERR} Line {index + 1} in {model_file.name} is not in the correct format:"
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

        _spec = SimSpec(spec, model_file, output_file, command=command)

        # add the variables to the spec
        for var, val in specfile[spec].items():
            _spec.add_iter_var(line_nums[var], val)

        # append the current spec to the list of specs
        specs.append(_spec)
    return specs


def run_simulation(
    spec: SimSpec, *, tmp_file: Path = Path("./_tmp_model_.modest")
) -> pd.DataFrame | None:
    """Runs the simulation specified
    
    Required inputs:
    - spec: a simualtion spec in the form of a SimSpec class instance
    
    Optional inputs:
    - tmp_file: the path to the temporary .modest file created for simulation
    
    Returns:
    - pd.DataFrame | None: A dataframe with the simulation data if successful, or None if not"""

    printv(f"{Fore.GREEN}Starting simulation for {spec.name}{Style.RESET_ALL}")

    printv(f"Opening {spec.model.name}")
    with spec.model.open("r") as f:
        model_lines = f.readlines()

    var_permutation = None
    len_range: int = 0

    # Get the iterator to the permutations of the inputs as well as the total number
    # of iterations
    (var_permutation, len_range) = permute_ranges(*(spec.vars_to_list()))

    # tqdm bar messes up when other output is enabled, so if verbose mode is on
    # the progess bar needs to be turned off
    if verbose:
        printv(f"Verbose mode is enabled, disabling tqdm status bar")
    else:
        var_permutation = tqdm(var_permutation, desc=f"{spec.name}", total=len_range)

    if var_permutation is None:
        print(
            f"{ERR} Variable permutation failed for {spec.name}"
        )
        return None

    # create the pandas dataframe to hold all the needed information
    # starts as None because we have no data
    sim_data: pd.DataFrame | None = None

    for range_vars in var_permutation:
        printv(f"Simulating permuation: {range_vars}")

        # create a temporary DataFrame to store this iterations data
        single_iter_data = {}

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
                    f"{ERR} Failed to find a const variable on line {line_num + 1} of {spec.model.name} while simulating {spec.name}"
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
        out = out.decode("utf-8", "ignore").split("\n")
        out2 = '\n'.join(out).rstrip();
        printv(f"Modest output:{Style.DIM}\n{out2}{Style.RESET_ALL}")
        printv(f"Finished simulation, finding properties")

        # capture probabilities and properties by name
        prob: float | None = None
        prop: str | None = None

        # create a tracker to track if all probabilities are 1
        prob_tracker: float = 1.0

        for line in out:
            # match each line with the property and probability regex
            prop_name = MODEST_PROPERTY_NAME_RE.match(line)
            prob_val = MODEST_PROBABILITY_RE.match(line)

            # if we get a match for property or probability store the value
            if not prop_name is None:
                prop = prop_name.group(1)

            if not prob_val is None:
                prob = prob_val.group(1)

            # since the property name and probability should be one line after the other
            # we can keep track if both of them are set. If they both are then we must
            # be reading in a new property, so we can save that to our data.
            if not (prop is None or prob is None):
                printv(f"\tFound {prop} = {prob}")
                single_iter_data[prop] = prob

                # used to check if all probabilities are 1. If all are 1, 1*1*1*1 == 1, so we can
                # check that to save simulation time
                prob_tracker *= float(prob)

                # reset the property name and probability trackers so that we can find another one (if there is one)
                prop = None
                prob = None

        # put all the information from this iteration of the permuted inputs into a dataframe
        single_iter_df = pd.DataFrame(single_iter_data, index=[1])

        # save the data into the overall dataframe
        if sim_data is None:
            sim_data = single_iter_df
        else:
            sim_data = pd.concat([sim_data, single_iter_df])

        # check if all probabilities are 1
        if prob_tracker >= 1.0:
            printv(f"All probabilities are 1.0, ending simualtion for {spec.name}")
            break

    # remove the temporary simulation file
    printv(f"Removing temporary file {tmp_file}")
    if tmp_file.exists():
        os.remove(tmp_file)

    # write the data to the output file in csv format
    printv(f"Writing simulation data to {spec.output}")
    sim_data.to_csv(spec.output, index=False)

    # return the data as well, in case it is to be used
    return sim_data


if __name__ == "__main__":
    # Define the argument parser
    args = get_parser().parse_args()

    print(f"{Fore.YELLOW}--- MODEST Simulation Runner ---{Style.RESET_ALL}")

    # Usage and credits
    print()
    print(f"  Usage: See README.md for instructions and examples")
    print(f"Version: {SCRIPT_VERSION}")
    print(f" Author: {SCRIPT_AUTHOR}")
    print(f"  Email: {SCRIPT_AUTHOR_EMAIL}")

    # check if verbose mode is enabled
    if args.verbose:
        verbose = True
        print()
        print(f"{Fore.CYAN}--- Verbose mode enabled ---{Style.RESET_ALL}")
        print(
            f"All verbose outputs will be annotated with a {Fore.CYAN}(v){Style.RESET_ALL}"
        )

    # check if modest is installed
    if shutil.which("modest") is None:
        print(f"{ERR} Could not find modest installation. Please add modest to the path")

    # check the spec file
    specfile_path = check_specfile_path(args.specfile)
    if specfile_path is None:
        print(
            f"{ERR} Simulation specification .toml file is not valid. Looked for file at:"
        )
        print(f"{args.specfile}")
        sys.exit()
    else:
        print()
        print(f"{Fore.GREEN}Successfully located specification file at {specfile_path}{Style.RESET_ALL}")

    # parse the spec file
    specs = get_specs(specfile_path)
    if specs is None:
        print(
            f"{Fore.RED}Simulation specifications could not be parsed{Style.RESET_ALL}"
        )
        sys.exit()
    else:
        print(f"{Fore.GREEN}Successfully parsed specifications from {specfile_path.name}{Style.RESET_ALL}")
    # run the simulations
    print()
    print(f"{Fore.YELLOW}--- Starting Simulations ---{Style.RESET_ALL}")

    for spec in specs:
        sim_output = run_simulation(spec)
        printv(f"Run simulation output:\n{Style.DIM}{sim_output}{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}--- Finished Simulations ---{Style.RESET_ALL}")

else:
    sys.exit("This is not a module to be imported!")
