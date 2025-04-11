# Goals 

# 1. Batch generate FMCAD results using the rewards model
#   - Need a way of generating models in Python with parameterization
#   - Ideall something like `noc_4x4 = noc(4)`
# 2. Generate resistive noise results for each model
#   - need a way to stop once probability == 1.0
#   - need a way to store the probabilities
#   - need a way to specify stride and upper clock bound
#   - something like `noc_4x4(filename, stride=2, upper_clk=300)`
# 3. Generate inductive noise results for each model
#   - same as above
# 4. Run functional correctness for each model
#   - Something like `noc_4x4.correct()` would be good

# Proposed project structure
#   - `noc` Class that can build a NoC. Customizable values can be
#   stored f-strings wrapped in a function
#   - `modest` class that runs and outputs models. Maybe has options like
#   `modest.simulate(input, output)` and `modest.check(input, output)`.
#   this class _could_ have the output parsing ability, or we could delegate
#   that to another class.

from noc import Noc, NoiseType
import csv
import modest
import time
from probabilities import parse_probabilities
from pathlib import Path

def simulate(*, result_path: Path = Path("results"), size: int, type: NoiseType, clk_upper: int | None, threshold: int = 1, stride : int = 1, block_size : int = 50):
    # Create result directory
    result_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize the NoC
    noc = Noc(size, resistive_noise_threshold=threshold, inductive_noise_threshold=threshold)

    # Print starting message
    print(f"Starting {noc._n}x{noc._n} {type.name} simulation...")
    clk = 0
    probs = []

    # The block size is how many properties to count at once. If we have a stride > 1 then
    # we need to multiply the block size by the stride to get the the correct number of 
    # properties tested at a single time
    block_size *= stride

    # Start the sim counter
    start_time = time.time()

    # Simulation
    while clk_upper is None or clk <= clk_upper:
        lower = clk 
        upper = clk + block_size - 1 

        if clk_upper is not None and upper > clk_upper:
            upper = clk_upper
            
        sim_output = modest.simulate(noc.print(type, lower, upper, stride))
        probs += parse_probabilities(sim_output)
        clk += block_size

        if max(probs, key=lambda x: x[1])[1] >= threshold:
            break
    
    # Timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    timing_file = result_path / Path(f"noc_{noc._n}x{noc._n}_{type.name.lower()}_noise_threshold_{threshold}_stride_{stride}_block_size_{block_size}.time.txt")

    # Format elapsed time as HH:MM:SS
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    time_str = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)

    output_str = f"Simulation parameters:\n"
    output_str += f"  Size: {noc._n}x{noc._n}\n"
    output_str += f"  Noise Type: {type.name}\n"
    output_str += f"  Clock Upper Bound: {clk_upper}\n"
    output_str += f"  Threshold: {threshold}\n"
    output_str += f"  Stride: {stride}\n"
    output_str += f"  Block Size: {block_size}\n"
    output_str += f"\n"
    output_str += f"Elapsed time: {time_str}\n"

    print(output_str)

    with open(timing_file, "w") as f:
        f.write(output_str)

    # Probabilities
    filename = result_path / Path(f"noc_{noc._n}x{noc._n}_{type.name.lower()}_noise_threshold_{threshold}_stride_{stride}_block_size_{block_size}.csv")
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Clock Cycle", "Probability"])
        writer.writerows(probs)

    return probs 
            
def noc_2x2_resistive():
    """ 2x2 resistive simulations """
    simulate(size=4, result_path=Path("2x2/results"), type=NoiseType.RESISTIVE, threshold=1, clk_upper=None, stride=1)
    simulate(size=4, result_path=Path("2x2/results"), type=NoiseType.RESISTIVE, threshold=5, clk_upper=None, stride=2)
    simulate(size=4, result_path=Path("2x2/results"), type=NoiseType.RESISTIVE, threshold=10, clk_upper=None, stride=5)
    simulate(size=4, result_path=Path("2x2/results"), type=NoiseType.RESISTIVE, threshold=20, clk_upper=None, stride=10)

if __name__ == "__main__":
    noc_2x2_resistive()
