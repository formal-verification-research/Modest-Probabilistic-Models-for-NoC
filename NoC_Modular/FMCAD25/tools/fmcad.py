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
import modest
from probabilities import parse_probabilities

noc = Noc(4)

clk_upper = 10
block_size = 2
clk = 0

probs: list[float] = []

while clk <= clk_upper:
    sim_output = modest.simulate(noc.print(NoiseType.RESISTIVE, clk, clk + block_size - 1))
    probs += parse_probabilities(sim_output)
    clk += block_size

    if max(probs) >= 1.0:
        break

print(probs)