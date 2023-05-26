# Modular Design of a Probabilistic NoC Model
This project contains:
* The Modest code for a modular NoC model. The model is configured into both a 2x2 and 3x3 mesh topologies.
* The data collected by simulation of both the 2x2 and 3x3 NoCs.
* Data collected from the previous
[Concrete](https://github.com/formal-verification-research/Modest-Probabilistic-Models-for-NoC/blob/master/FMICS2021/concrete.modest) 
model, as well as the previous
[Abstracted](https://github.com/formal-verification-research/Modest-Probabilistic-Models-for-NoC/blob/master/FMICS2021/predicateAbstract.modest)
model.

## Verification of the Probabilistic Model 
The modular model presented in this project was verified using simulation methods via the Modest Toolset version v3.1.182-g3d5d3ecdf.

Simulation can be performed using the command:

`modest simulate --max-run-length 0 concrete2x2.modest`

The upper clock can be modified in the code using the `CLK_UPPER` constant. The thresholds for both resistive and inductive noise can be modified using the `RESISTIVE_NOISE_THRESH` and `INDUCTIVE_NOISE_THRESH` constants respectively.

A [script](https://github.com/formal-verification-research/Modest-Probabilistic-Models-for-NoC/blob/master/NoC_Modular/Plots/runner.py) exists to simulate multiple execution. This was used to generate the plot data found in [this](https://github.com/formal-verification-research/Modest-Probabilistic-Models-for-NoC/tree/master/NoC_Modular/Plots/Data) directory. The format for running the script is:

`python3 runner.py <ModelPath> <OutputFileName> <LineWhere-CLK_UPPER-IsDefined> <StartClock:Interval:EndClock>`

For example, the following command would execute simulation runs of the 2x2 NoC, for 4, 6, and 8 clock cycles:

`python3 runner.py ../concrete2x2.modest data.csv 38 4:2:8`

## Representing Data
The data generated in this work is plotted using MatLab tools, and can be viewed via the .mlx file fond in the [Plots](https://github.com/formal-verification-research/Modest-Probabilistic-Models-for-NoC/tree/master/NoC_Modular/Plots) directory.
