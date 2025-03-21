import process_cex
import subprocess
import os
from pathlib import Path
import argparse

def generate_cex(dfy_file: Path):
    """
    Generates a counterexample for the given Dafny file.

    Args:
        dfy_file (str): The path to the Dafny file.
    """
    # Run Dafny to generate a counterexample.
    result = subprocess.run(
        [
            "dafny",
            "verify",
            "--extract-counterexample",
            dfy_file,
        ],
        capture_output=True,
        text=True,
    )

    # Extract the counterexample from the output.
    output = (result.stdout + result.stderr)

    print(process_cex.format_document(output, color=True))

def main():
    parser = argparse.ArgumentParser(
        description="Generate a counterexample for a Dafny file."
    )
    parser.add_argument("dfy_file", help="Path to the Dafny file")
    args = parser.parse_args()

    generate_cex(Path(args.dfy_file))

if __name__ == "__main__":
    main()
