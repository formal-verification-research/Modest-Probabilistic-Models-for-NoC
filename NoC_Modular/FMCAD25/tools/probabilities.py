# Expected input:

#  + Property resistiveNoiseProbability1RewardBounded0
#     Estimated probability: 0
#     Runs used:             490

#     + Error bounds
#       Statement: Adaptive: P(error > ε) < δ
#       ε:         0.01
#       δ:         0.050000000000000044

#   + Property resistiveNoiseProbability1RewardBounded1
#     Estimated probability: 0.2700947225981056
#     Runs used:             14780

#     + Error bounds
#       Statement: Adaptive: P(error > ε) < δ
#       ε:         0.01
#       δ:         0.050000000000000044

#   + Property resistiveNoiseProbability1RewardBounded2
#     Estimated probability: 0.5107859078590786
#     Runs used:             18450

#     + Error bounds
#       Statement: Adaptive: P(error > ε) < δ
#       ε:         0.01
#       δ:         0.050000000000000044

import re

def parse_probabilities(output: str) -> list[tuple[int, float]]:
    """Parses the output of the Modest tool to extract probabilities.

    Args:
        output: The output string from the Modest tool.

    Returns:
        A list of floats representing the extracted probabilities.
    """
    probabilities = []
    pattern = r"Property \w+Probability\w+RewardBounded(\d+)\s+Estimated probability:\s+([\d.]+)"
    matches = re.findall(pattern, output)
    
    # Sort matches by the number in the property name
    matches.sort(key=lambda x: int(x[0]))

    for cycle, probability in matches:
        probabilities.append((int(cycle), float(probability)))

    print(probabilities)
    return probabilities
