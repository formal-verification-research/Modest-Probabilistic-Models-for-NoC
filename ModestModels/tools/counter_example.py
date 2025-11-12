#!/usr/bin/env python3
import re
import argparse
from typing import Callable
import subprocess
from pathlib import Path

def process_line(line):
    # If the line starts with a number (optionally with spaces) followed by a vertical bar,
    # then leave the line unchanged.
    if re.match(r'^\s*\d+\s*\|', line):
        return line
    # Insert a newline and a tab after each "&&"
    return re.sub(r'\s*&&\s*', r' &&\n\t', line)

def format_output(doc: str, *, color: bool = False) -> str:
    # Process each line from the original file.
    formatted = '\n'.join([process_line(line) for line in doc.splitlines()])

    if color:
        # brackets (these have to come first)
        formatted = formatted.replace("[", "\033[37m[\033[0m")
        formatted = formatted.replace("]", "\033[37m]\033[0m")
        formatted = formatted.replace("(", "\033[37m(\033[0m")
        formatted = formatted.replace(")", "\033[37m)\033[0m")
        formatted = formatted.replace("{", "\033[37m{\033[0m")
        formatted = formatted.replace("}", "\033[37m}\033[0m")

        # keywords + operators
        formatted = formatted.replace("==", "\033[91m==\033[0m")
        formatted = formatted.replace("<=", "\033[91m<=\033[0m")
        formatted = formatted.replace(">=", "\033[91m>=\033[0m")
        formatted = formatted.replace("!=", "\033[91m!=\033[0m")
        formatted = formatted.replace("&&", "\033[91m&&\033[0m")
        formatted = formatted.replace("||", "\033[91m||\033[0m")
        formatted = formatted.replace(" < ", " \033[91m<\033[0m ")
        formatted = formatted.replace(" > ", " \033[91m>\033[0m ")
        formatted = formatted.replace("?", "\033[91m?\033[0m")
        formatted = formatted.replace("$", "\033[91m$\033[0m")
        formatted = formatted.replace("assume", "\033[91massume\033[0m")
        formatted = formatted.replace("ensures", "\033[91mensures\033[0m")

        # this
        formatted = formatted.replace("this", "\033[0;33mthis\033[0m")

    return formatted 

type Filter = Callable[[str], bool]

def default_filter(line: str) -> bool:
    return "!in" in line
    
def filter_document(doc: list[str], filter: Filter) -> list[str]:
    # Now, split the formatted content into physical lines, filter out any line containing '!in'
    return [line for line in doc if not filter(line)]

def run_dafny_file(file_path: Path) -> str:
    """
    Runs a Dafny file and returns the output as a UTF-8 string.

    Args:
        file_path: The path to the Dafny file.

    Returns:
        The output of the Dafny program as a UTF-8 string.
    """
    try:
        result = subprocess.run(["dafny", "verify", str(file_path), "--extract-counterexample"], capture_output=True, text=True, encoding="utf-8", check=True)
        return result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout + e.stderr


def main():
    parser = argparse.ArgumentParser(
        description="Pretty prints counter examples from Dafny."
    )
    parser.add_argument("Input", help="Path to the dafny file")
    args = parser.parse_args()

    dfy_output = run_dafny_file(args.Input)
    formatted_output = format_output(dfy_output, color=True)

    print(formatted_output)

if __name__ == "__main__":
    main()
