#!/usr/bin/env python3
import re
import argparse
from typing import Callable

def process_line(line):
    # If the line starts with a number (optionally with spaces) followed by a vertical bar,
    # then leave the line unchanged.
    if re.match(r'^\s*\d+\s*\|', line):
        return line
    # Insert a newline and a tab after each "&&"
    return re.sub(r'\s*&&\s*', r' &&\n\t', line)

def format_document(doc: list[str], *, color: bool = False) -> str:
    # Process each line from the original file.
    formatted = '\n'.join([process_line(line) for line in doc])

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

def main():
    parser = argparse.ArgumentParser(
        description="Format a text file by inserting a newline and a tab after each '&&', except on lines that begin with a number and '|'. Then, filter out lines containing '!in' from the formatted output."
    )
    parser.add_argument("input", help="Path to the input text file")
    # parser.add_argument("output", help="Path to the output text file (formatted file)")
    # parser.add_argument("filtered", help="Path to the filtered text file (formatted file with lines containing '!in' removed)")
    # parser.add_argument("--in-enc", default="utf-16-le", help="Input file encoding (default: utf-16-le)")
    # parser.add_argument("--out-enc", default="utf-8", help="Output file encoding (default: utf-8)")
    args = parser.parse_args()

    # Read the original file.
    with open(args.input, 'r') as infile:
        lines = infile.readlines()

    formatted_content = format_document(lines)

    print(formatted_content)
    return

    with open(args.output, 'w', encoding=args.out_enc, newline='') as outfile:
        outfile.write(formatted_content)


    physical_lines = formatted_content.splitlines(keepends=True)
    filtered_lines = filter_document(physical_lines)

    # Write the filtered content to the third file.
    with open(args.filtered, 'w', encoding=args.out_enc, newline='') as f_filtered:
        f_filtered.write(''.join(filtered_lines))

if __name__ == "__main__":
    main()
