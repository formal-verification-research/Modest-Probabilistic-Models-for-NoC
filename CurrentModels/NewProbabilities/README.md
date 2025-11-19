# New Probabilities

This is an attempt to measure the probability of PSN at each router in each clock cycle
as opposed to measuring cumulative PSN.

Initial results of testing this out are in
[this directory](./results_2025_11_18_21_25_32/Resistive_new_prob_3x3_a3/), and show that
this method has promise.
[This plot](./results_2025_11_18_21_25_32/Resistive_new_prob_3x3_a3/plots_2025_11_19_13_21_49_of_Resistive_new_prob_3x3_a3/plot.pdf)
shows the probability that eventually within $K$ clock cycles the activity level of a
router will be above 3. This does _not_ guarantee the probability of a router having a
activity level of 3, but rather provides an upper bound of the activity level for each
router at each clock cycle.
