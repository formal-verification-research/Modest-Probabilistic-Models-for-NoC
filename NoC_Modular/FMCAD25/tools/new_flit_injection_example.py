from fmcad import simulate
from noc import PropertyType
from pathlib import Path

if __name__ == "__main__":
    # This demonstrates how to simulate the PSN results from a custom
    # flit traffic pattern. In this example the flit pattern is one where
    # flits are sent non-deterministically in a burst pattern where
    # the duty cycle varies between 5% and 25% for each router
    
    custom_generate_flits = """
int[] burst_times = [0, 0, 0, 0];
int[] sleep_times = [0, 0, 0, 0];
const int BURST_MIN = 10;
const int BURST_MAX = 100;
const int SLEEP_MIN = 200;
const int SLEEP_MAX = 400;
process GenerateFlits(int id) {
    int(0..NOC_MAX_ID) destination;

    if (isBufferFull(noc[id].channels[LOCAL].buffer)) {
        generateFlits // Take this action instead of tau for better synchronization
    } else {
        // This custom process sends a flit in a bursty pattern
        if (burst_times[id] != 0) {
            generateFlits {=
                0: destination = DiscreteUniform(0, NOC_MAX_ID - 1),
                1: noc[id].channels[LOCAL].buffer = 
                    enqueue(destination >= id ? 
                                destination + 1 : 
                                destination, noc[id].channels[LOCAL].buffer),
                2: burst_times[id] = burst_times[id] - 1
            =}
        } else if (sleep_times[id] != 0) {
            generateFlits {=
                sleep_times[id] = sleep_times[id] - 1
            =}
        } else {
            generateFlits {=
                burst_times[id] = DiscreteUniform(BURST_MIN, BURST_MAX),
                sleep_times[id] = DiscreteUniform(SLEEP_MIN, SLEEP_MAX)
            =}
        }
    }
}
"""

    print("Running simulation with custom flit generation...")

    # Run a single 2x2 resistive noise simulation with the custom flit generation.
    simulate(
        size=2,
        result_path=Path("results/2x2_custom_flit_gen"),
        type=PropertyType.RESISTIVE,
        threshold=5,
        clk_upper=None,
        stride=1,
        generate_flits=custom_generate_flits,
    )
