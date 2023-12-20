# Author: Nick Waddoups

import argparse
import sys
import tomlkit
from pathlib import Path
from colorama import Fore, Style

# Global variables
verbose: bool = False


# Functions
def printv(*values: object, sep: str | None = " ", end: str | None = "\n") -> None:
    if verbose:
        print(*values, sep=sep, end=end)


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

def check_specfile_contents(path: Path) -> dict | None:
    """Checks if the contents of the spec file are valid"""
    with path.open() as f:
        specfile_as_str: str = f.read()

    specfile: dict = tomlkit.parse(specfile_as_str).unwrap()

    for spec in specfile:
        printv(f"Found spec {spec}, parsing:")

        # intially set model_file to None, this is how we check if there was a file arg or not
        model_file: Path | None = None

        # iterate over all of the details
        for detail, val in specfile[spec].items():
            printv(f"\t{detail} = {val}")

            # check if this is a file argument
            if detail.lower() == "file":
                # check if it's a valid file
                model_file = Path(val)
                if not model_file.exists():
                    print(f"File {val} does not exist.")
                    print(f"To fix update the filepath for {spec} in {path.name}.")
                    return None
        
        # after iterating over the details check if a file was passed in
        if model_file is None:
            print(f"Spec {spec} does not contain a 'file' member.")
            print(f"To fix add 'file = \"<path to modest file>\" in {path.name}")
            return None
        
        # Then check if all of the requested iteration variables are in the modest file
        with model_file.open() as f:
            lines = f.readlines()
        
        # TODO: Implement class for storing all this data, probably like this:
        # Root
        #   > Name: str
        #   > File: Path
        #   > vars: Dict{str, range}
                

    return specfile


if __name__ == "__main__":
    # Define the argument parser
    args = get_parser().parse_args()

    if args.verbose:
        verbose = True
        print(f"Verbose mode enabled")

    # check the spec file
    specfile_path = check_specfile_path(args.specfile)
    if specfile_path is None:
        sys.exit()

    specfile = check_specfile_contents(specfile_path)


else:
    sys.exit("This is not a module to be imported!")
