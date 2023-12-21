# MODEST Simulation Runner

Run many Modest simulations in a row while iterating over constants inside of a modest model using a TOML file
as a simulation specification.

## About

This tool came about while I was trying to collect data on resistive and inductive noise generated
by the modular and monolithic NoC models written in the Modest language. To gather this data we run
hundreds of DTMC Modest simulations that iterate over a variable, typically the `CLK_COUNT` (or 
`CLK_UPPER`, `DUR`, etc.) variable and then capturing the probability of some property after the simulation
was run. This process was previously automated before but the automation script failed to meet the
needs for truly massive simulations, as only one variable could be iterated over at a time and only
one simulation set could be run at a time.

I had the desire to separate the simulation specification (parameters) into a separate file that could be
consumed by a script that would run all the simulations. Thus this tool was born, and now you can specify
simulation specifications in a TOML file, and run all the simulations using this script.

Contact me at [nick.waddoups@usu.edu](mailto:nick.waddoups@usu.edu) if you have questions!

## Requirements

1. `python3` is installed, and
2. `modest` is located on the path

## Installation

Download this script and accompanying directory from GitHub, then install the required python packages.

It's recommended that you install a virtual python environment to use this script. If you choose not to
the steps are mostly the same however.

### Using a Virtual Environment

Once the virtual environment is activated, install all the required packages using the following command:

```bash
pip install -r requirements.txt
```

Then the script should be able to be run whenever the virtual environment is active

### Without a Virtual Environment

This is not recommended as a requirements.txt file is used by this project, which will possibly install older versions of
packages which could cause issues for other projects on your machine. To avoid this follow the instructions
[here](https://docs.python.org/3/library/venv.html) to set up a virtual environment on your machine.

If you choose not to use a virtual environment, install the required packages by running:

```bash
python3 -m pip install -r requirements.txt
```

## Usage

To run simply type:

```bash
python3 run.py <simulation_specification>.toml
```

The script will then parse the toml file and begin running the simulations.

## TOML Simulation Specification

The format for making a simulation specification is as follows:

```toml
[Name_of_Specification_1]
_model_ = "Path to .modest model file" # Required var
_output_ = "Path to .csv or .txt output file" # Required var
_command_ = "simulate --max-run-length 10" # Optional var
VAR_1 = "1:1"
VAR_2 = "1:1:100"
# ...
VAR_N = "2:2:16"

[Name_of_Specification_2]
# ...

[Name_of_Specification_N]
```

Here is a general breakdown of what each part does

### Title:

```toml
[Name_of_Specification]
```

This is where the title of the simulation specification goes. There can be as many specification as
desired, but within one TOML file **each individual must have a unique name**. These names will be displayed
while the simulation is running, so it may be helpful to use a useful name here.

### Simulation Tool Variables

```toml
# ...
_model_ = "Path to .modest model file" # Required var
_output_ = "Path to .csv or .txt output file" # Required var
_command_ = "simulate --max-run-length 10" # Optional var
# ...
```

These variables are used in actually running the simulation, and do not represent Modest variables
to be iterated over. Note that because these variables are used for simulation options it means that
there cannot be a Modest variable named `_model_`, `_output_`, or `_command_` in the model being
simulated. Hopefully this does not cause an issue.

#### Required Variables

These variables are required to be present in **every simulation specification**, but the order in
which they appear does not matter.

1. `_model_` - This is the file path to the .modest model. Note that this path should either be absolute or relative to the location of the run.py script.
2. `_output_` - This is the file path to the output file, where the data from this simulation will be stored. This must be a .txt or a .csv file, and all output data will be stored in .csv format using ascii encoding.

#### Optional Variables

These variables are used during simulation, but are not required.

1. `_command_` - changes the modest command to be used. The default command is `simulate --max-run-length 0` but could be changed to something else. For example, to do model checking it could be changed to `check`. This command should not include the `modest` executable name or the path to the .modest model file.

### Iteration Variables

```toml
VAR_1 = "1:1"
VAR_2 = "1:1:100"
# ...
VAR_N = "2:2:16"
```

These are variables that are within your Modest model and you want to iterate over. Make sure the name
of the variable in the TOML file matches the name of the variable in the Modest model *exactly*. The script will attempt to automatically locate all of the variables you ask it to in the model file you give it, and if it does not find a match it will not run the simulations.

These variables should be in the format:

```toml
[Spec_name]
# ...
var_name = "range"
```

Where `var_name` is the variable to be iterated over in the model, and `range` is the range which it should be iterated over. Acceptable formats for range are:

1. `"<start>:<end>"` - Generates a range from start to end with a step size of 1
2. `"<start>:<step>:<end>"` - Generates a range from start to end with a specified step size

#### Examples of Iteration Variables

```toml
CLK_UPPER = "1:1:2" # will simulate the model twice for this var
# CLK_UPPER == [1, 2]

DUR = "1:10" # will simulate the model 10 times for this var
# DUR == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

BUFFER_DEPTH = "3:3" # This is a way to set a const value, instead of a range
# BUFFER_DEPTH == 3
```

As you add more iteration variables, the number of simulations to run increases exponentially. In the previous example
we have three variables, `CLK_UPPER`, `DUR`, and `BUFFER_DEPTH`. The total number of simulations run is the length of
each of these variables multiplied by each other.

For the previous example, `num_simulations = len(CLK_UPPER) * len(DUR) * len(BUFFER_DEPTH) = 2 * 10 * 1 = 20`. Twenty Modest
simulations could take hours or longer depending on the model that you are using, so take care to only iterate over variables
when you need to.

## Examples

There is an example TOML file and modular NoC model given in this repository. Use these as a starting point if
you need.

## TODOs

Ideally I would like to add a feature where you could pass a list of numbers for a variable in the toml file,
like so:

```toml
ACTIVITY_THRESH = "1,3,7,15"
```

but this is currently not implemented.
