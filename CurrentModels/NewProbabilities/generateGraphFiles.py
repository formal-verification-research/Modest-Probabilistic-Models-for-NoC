from pathlib import Path
from pathvalidate import sanitize_filename
from datetime import datetime
import sys

if __name__ == "__main__":
    # Check inputs
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path to results dir>")
        exit(1)
    
    # Locate the script directory
    script_dir = Path(__file__).resolve().parent

    # Get the output directory
    output_dir = Path(sys.argv[1])
    if not output_dir.exists():
        print(f"Output directory supplied, ``{sys.argv[1]}'', was not found.")
        exit(1)
    else:
        output_dir = output_dir.resolve()

    # Setup the output directory
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_dir = script_dir / sanitize_filename(f"plots_{timestamp}_of_{output_dir.name}")
    output_dir.mkdir()

    # For each child directory, generate plot files (to go in latex)