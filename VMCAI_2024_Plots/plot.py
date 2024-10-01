import matplotlib.pyplot as plt
import csv

def get_array(file: str):
    with open(file) as f:
        csv_f = csv.reader(f)

        plain_data = []

        for row in csv_f:
            for data in row:
                plain_data.append(data)
        
        clock = [(plain_data[i]) for i in range(0, len(plain_data)-1, 2)]
        data = [(plain_data[i+1]) for i in range(0, len(plain_data)-1, 2)]

        return (clock, data)

r_22_1 = get_array('/Users/nick/Documents/Programming/Modest-Probabilistic-Models-for-NoC/NoC_Modular/Plots/Data/Jonah/Resistive/post_2x2_1.csv')
r_22_5 = get_array('/Users/nick/Documents/Programming/Modest-Probabilistic-Models-for-NoC/NoC_Modular/Plots/Data/Jonah/Resistive/post_2x2_5.csv')
r_22_10 = get_array('/Users/nick/Documents/Programming/Modest-Probabilistic-Models-for-NoC/NoC_Modular/Plots/Data/Jonah/Resistive/post_2x2_10.csv')
r_22_20 = get_array('/Users/nick/Documents/Programming/Modest-Probabilistic-Models-for-NoC/NoC_Modular/Plots/Data/Jonah/Resistive/post_2x2_20.csv')

# Create the plot
plt.figure()

# Plot the lines
plt.plot(r_22_1[0], r_22_1[1], label='>= 1')
plt.plot(r_22_5[0], r_22_5[1], label='>= 5')
plt.plot(r_22_10[0], r_22_10[1], label='>= 10')
plt.plot(r_22_20[0], r_22_20[1], label='>= 20')

# Set up the plot
plt.xlabel('Clock Cycle')
plt.ylabel('Probability of Resistive Noise')
plt.grid(True)
plt.legend(fontsize=6)

# Set font size for tick labels

# Adjust layout to prevent cutting off labels
# plt.tight_layout()

# Show the plot
plt.show()