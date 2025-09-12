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

from noc import Noc, PropertyType
import csv
import modest
import time
from probabilities import parse_probabilities
from pathlib import Path

def time_to_str(time: float) -> str:
    """Format time as HH:MM:SS"""
    hours, rem = divmod(time, 3600)
    minutes, seconds = divmod(rem, 60)
    time_str = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)
    return time_str

def time_func(func):
    """Decorator to time a function's execution."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_str = time_to_str(elapsed_time)
        print(f"[status]: Function '{func.__name__}' took {time_str} to execute.\n")
        return result
    return wrapper

def check(*, result_path: Path = Path("results"), size: int, type: PropertyType, clk_upper: int | None, threshold: int = 1, stride : int = 1, block_size : int = 50, generate_flits: str | None = None):
    # Create result directory
    result_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize the NoC
    noc = Noc(size, resistive_noise_threshold=threshold, inductive_noise_threshold=threshold)

    # Print starting message
    output_str = f"Modest check parameters:\n"
    output_str += f"  Size: {noc.dimension}x{noc.dimension}\n"
    output_str += f"  Noise Type: {type.name}\n"
    output_str += f"  Clock Upper Bound: {clk_upper}\n"
    output_str += f"  Threshold: {threshold}\n"
    output_str += f"  Stride: {stride}\n"
    output_str += f"  Block Size: {block_size}\n"
    print(output_str, end="")
    print(f"\nStarting {noc.dimension}x{noc.dimension} {type.name} simulation...")

    # Initialize variables
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
            
        sim_output = modest.check(noc.print(type, clk_low=lower, clk_high=upper, stride=stride, generate_flits=generate_flits))
        new_probs = parse_probabilities(sim_output)
        clk += block_size

        if len(new_probs) > 0:
            probs += new_probs
            pmax = max(probs, key=lambda x: x[1])[1]

            print(f"  [info]: finished clock cycle block ({lower},{upper}). P: [", end="")        
            print(*[f"{p[1]:.3f}" for p in probs[lower:lower+3]], sep=", ", end="")
            print("...", end="")        
            print(*[f"{p[1]:.3f}" for p in probs[-3:]], sep=", ", end="")
            print(f"]. Pmax: {pmax:.3f}")
        else:
            print(f"  [info]: finished clock cycle block ({lower},{upper}) but probs were not calculated") 

        output_str += f"\n{sim_output}\n"

        if pmax >= (1.0 - 1e-5):            
            break
    
    # Timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    timing_file = result_path / Path(f"noc_{noc.dimension}x{noc.dimension}_{type.name.lower()}_noise_threshold_{threshold}_stride_{stride}_block_size_{block_size}.time.txt")
    time_str = time_to_str(elapsed_time)

    # Print out the time string
    print(f"Simulation complete. Time elapsed: {time_str}\n")

    # Write the output string to the output file
    output_str += f"\n"
    output_str += f"Total elapsed time: {time_str}\n"
    with open(timing_file, "w") as f:
        f.write(output_str)

    # Probabilities
    filename = result_path / Path(f"noc_{noc.dimension}x{noc.dimension}_{type.name.lower()}_noise_threshold_{threshold}_stride_{stride}_block_size_{block_size}.csv")
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Clock Cycle", "Probability"])
        writer.writerows(probs)

    return probs 

def simulate(*, result_path: Path = Path("results"), size: int, type: PropertyType, clk_upper: int | None, threshold: int = 1, stride : int = 1, block_size : int = 50, generate_flits: str | None = None):
    # Create result directory
    result_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize the NoC
    noc = Noc(size, resistive_noise_threshold=threshold, inductive_noise_threshold=threshold)

    # Print starting message
    output_str = f"Simulation parameters:\n"
    output_str += f"  Size: {noc.dimension}x{noc.dimension}\n"
    output_str += f"  Noise Type: {type.name}\n"
    output_str += f"  Clock Upper Bound: {clk_upper}\n"
    output_str += f"  Threshold: {threshold}\n"
    output_str += f"  Stride: {stride}\n"
    output_str += f"  Block Size: {block_size}\n"
    print(output_str, end="")
    print(f"\nStarting {noc.dimension}x{noc.dimension} {type.name} simulation...")

    # Initialize variables
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
            
        sim_output = modest.simulate(noc.print(type, clk_low=lower, clk_high=upper, stride=stride, generate_flits=generate_flits))
        new_probs = parse_probabilities(sim_output)
        clk += block_size

        if len(new_probs) > 0:
            probs += new_probs
            pmax = max(probs, key=lambda x: x[1])[1]

            print(f"  [info]: finished clock cycle block ({lower},{upper}). P: [", end="")        
            print(*[f"{p[1]:.3f}" for p in probs[lower:lower+3]], sep=", ", end="")
            print("...", end="")        
            print(*[f"{p[1]:.3f}" for p in probs[-3:]], sep=", ", end="")
            print(f"]. Pmax: {pmax:.3f}")
        else:
            print(f"  [info]: finished clock cycle block ({lower},{upper}) but probs were not calculated") 

        output_str += f"\n{sim_output}\n"

        if pmax >= (1.0 - 1e-5):            
            break
    
    # Timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    timing_file = result_path / Path(f"noc_{noc.dimension}x{noc.dimension}_{type.name.lower()}_noise_threshold_{threshold}_stride_{stride}_block_size_{block_size}.time.txt")
    time_str = time_to_str(elapsed_time)

    # Print out the time string
    print(f"Simulation complete. Time elapsed: {time_str}\n")

    # Write the output string to the output file
    output_str += f"\n"
    output_str += f"Total elapsed time: {time_str}\n"
    with open(timing_file, "w") as f:
        f.write(output_str)

    # Probabilities
    filename = result_path / Path(f"noc_{noc.dimension}x{noc.dimension}_{type.name.lower()}_noise_threshold_{threshold}_stride_{stride}_block_size_{block_size}.csv")
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Clock Cycle", "Probability"])
        writer.writerows(probs)

    return probs 

@time_func
def noc_2x2_resistive():
    """ 2x2 resistive simulations """
    simulate(size=2, result_path=Path("results/2x2"), type=PropertyType.RESISTIVE, threshold=1, clk_upper=None, stride=1)
    simulate(size=2, result_path=Path("results/2x2"), type=PropertyType.RESISTIVE, threshold=5, clk_upper=None, stride=1)
    simulate(size=2, result_path=Path("results/2x2"), type=PropertyType.RESISTIVE, threshold=10, clk_upper=None, stride=4)
    simulate(size=2, result_path=Path("results/2x2"), type=PropertyType.RESISTIVE, threshold=20, clk_upper=None, stride=7)

@time_func
def noc_2x2_inductive():
    """ 2x2 inductive simulations """
    simulate(size=2, result_path=Path("results/2x2"), type=PropertyType.INDUCTIVE, threshold=1, clk_upper=None, stride=6)
    simulate(size=2, result_path=Path("results/2x2"), type=PropertyType.INDUCTIVE, threshold=5, clk_upper=None, stride=12)
    simulate(size=2, result_path=Path("results/2x2"), type=PropertyType.INDUCTIVE, threshold=10, clk_upper=None, stride=36)


@time_func
def noc_2x2_resistive_check():
    """ 2x2 resistive simulations with modest check """
    check(size=2, result_path=Path("results/2x2_check"), type=PropertyType.RESISTIVE, threshold=1, clk_upper=None, stride=1)
    check(size=2, result_path=Path("results/2x2_check"), type=PropertyType.RESISTIVE, threshold=5, clk_upper=None, stride=1)
    check(size=2, result_path=Path("results/2x2_check"), type=PropertyType.RESISTIVE, threshold=10, clk_upper=None, stride=4)
    check(size=2, result_path=Path("results/2x2_check"), type=PropertyType.RESISTIVE, threshold=20, clk_upper=None, stride=7)

@time_func
def noc_2x2_inductive_check():
    """ 2x2 inductive simulations with modest check """
    check(size=2, result_path=Path("results/2x2_check"), type=PropertyType.INDUCTIVE, threshold=1, clk_upper=None, stride=6)
    check(size=2, result_path=Path("results/2x2_check"), type=PropertyType.INDUCTIVE, threshold=5, clk_upper=None, stride=12)
    check(size=2, result_path=Path("results/2x2_check"), type=PropertyType.INDUCTIVE, threshold=10, clk_upper=None, stride=36)

@time_func
def noc_3x3_resistive():
    """ 3x3 resistive simulations """
    simulate(size=3, result_path=Path("results/3x3"), type=PropertyType.RESISTIVE, threshold=1, clk_upper=None, stride=1)
    simulate(size=3, result_path=Path("results/3x3"), type=PropertyType.RESISTIVE, threshold=5, clk_upper=None, stride=1)
    simulate(size=3, result_path=Path("results/3x3"), type=PropertyType.RESISTIVE, threshold=10, clk_upper=None, stride=1)
    simulate(size=3, result_path=Path("results/3x3"), type=PropertyType.RESISTIVE, threshold=20, clk_upper=None, stride=1)

@time_func
def noc_3x3_inductive():
    """ 3x3 inductive simulations """
    simulate(size=3, result_path=Path("results/3x3"), type=PropertyType.INDUCTIVE, threshold=1, clk_upper=None, stride=1)
    simulate(size=3, result_path=Path("results/3x3"), type=PropertyType.INDUCTIVE, threshold=5, clk_upper=None, stride=2)
    simulate(size=3, result_path=Path("results/3x3"), type=PropertyType.INDUCTIVE, threshold=10, clk_upper=None, stride=4)

@time_func
def noc_4x4_resistive():
    """ 4x4 resistive simulations """
    simulate(size=4, result_path=Path("results/4x4"), type=PropertyType.RESISTIVE, threshold=1, clk_upper=None, stride=1)
    simulate(size=4, result_path=Path("results/4x4"), type=PropertyType.RESISTIVE, threshold=5, clk_upper=None, stride=1)
    simulate(size=4, result_path=Path("results/4x4"), type=PropertyType.RESISTIVE, threshold=10, clk_upper=None, stride=1)
    simulate(size=4, result_path=Path("results/4x4"), type=PropertyType.RESISTIVE, threshold=20, clk_upper=None, stride=1)

@time_func
def noc_4x4_inductive():
    """ 4x4 inductive simulations """
    simulate(size=4, result_path=Path("results/4x4"), type=PropertyType.INDUCTIVE, threshold=1, clk_upper=None, stride=1)
    simulate(size=4, result_path=Path("results/4x4"), type=PropertyType.INDUCTIVE, threshold=5, clk_upper=None, stride=2)
    simulate(size=4, result_path=Path("results/4x4"), type=PropertyType.INDUCTIVE, threshold=10, clk_upper=None, stride=4)

@time_func
def noc_8x8_resistive():
    """ 8x8 resistive simulations """
    simulate(size=8, result_path=Path("results/8x8"), type=PropertyType.RESISTIVE, threshold=1, clk_upper=5, stride=1)
    simulate(size=8, result_path=Path("results/8x8"), type=PropertyType.RESISTIVE, threshold=5, clk_upper=5, stride=1)
    simulate(size=8, result_path=Path("results/8x8"), type=PropertyType.RESISTIVE, threshold=10, clk_upper=5, stride=1)
    simulate(size=8, result_path=Path("results/8x8"), type=PropertyType.RESISTIVE, threshold=20, clk_upper=5, stride=1)

@time_func
def noc_8x8_inductive():
    """ 8x8 inductive simulations """
    simulate(size=8, result_path=Path("results/8x8"), type=PropertyType.INDUCTIVE, threshold=1, clk_upper=40, stride=1)
    simulate(size=8, result_path=Path("results/8x8"), type=PropertyType.INDUCTIVE, threshold=5, clk_upper=40, stride=1)
    simulate(size=8, result_path=Path("results/8x8"), type=PropertyType.INDUCTIVE, threshold=10, clk_upper=40, stride=1)
    simulate(size=8, result_path=Path("results/8x8"), type=PropertyType.INDUCTIVE, threshold=20, clk_upper=40, stride=1)

if __name__ == "__main__":
    # Check to make sure that this script was called from above the tools directory
    if Path.cwd().name == "tools":
        raise Exception("This script must be called from the directory above 'tools'.\n"
                        "Example: python tools/fmcad.py")

    # Resistive Simulations
    noc_2x2_resistive()
    noc_2x2_resistive_check()
    noc_3x3_resistive()
    noc_4x4_resistive()
    noc_8x8_resistive()

    # Inductive Simulations
    noc_2x2_inductive()
    noc_2x2_inductive_check()
    noc_3x3_inductive()
    noc_4x4_inductive()
    noc_8x8_inductive()
