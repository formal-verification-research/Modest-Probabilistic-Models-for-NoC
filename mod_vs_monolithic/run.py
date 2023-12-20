# Author: Nick Waddoups

import argparse
import sys
import tomlkit
from pathlib import Path

# Global variables
verbose: bool = False

def get_parser():
    """This returns the argument parser for this script"""
    parser = argparse.ArgumentParser()
    parser.add_argument("specfile",
                        help="MODEST simulation specification file",
                        type=str)
    parser.add_argument("--verbose",
                        help="turn verbose comments on",
                        action="store_true")
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

def check_specfile_contents(specfile_path: Path) -> tomlkit.toml_document.TOMLDocument | None
    """Checks if the contents of the spec file are valid"""
    specfile = specfile_path

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
