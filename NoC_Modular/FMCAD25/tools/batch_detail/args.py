import argparse
from pathlib import Path
import batch_detail.strings as s

def get_parser() -> argparse.ArgumentParser:
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
        print(f"{s.ERR} Could not find simulation specification file at")
        print(f"{specfile}")
        return None

    # check if it's a toml file
    if not specfile.suffix.lower() == ".toml":
        print(f"{s.ERR} Simulation specification file {specfile} is not ", end="")
        print(f"a .toml file")
        return None

    return specfile

def parse() -> argparse.Namespace | None:
    """Parses the input arguments and checks if they are valid or not.

    Returns:
        argparse.Namespace | None: Either a valid argument list or None.
    """
    args = get_parser().parse_args()

    if check_specfile_path(args.specfile) is None:
        return None
    
    return args 
    