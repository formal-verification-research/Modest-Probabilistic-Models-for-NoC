## Readme for the abstract interpolation process version 4

# First abstract model

The process consists of two steps, creating an abstract model, then generating counter examples for the model.
This process is repeated until the abstract model generates no counter examples.

The first abstract model is the four state model defined below:

This states in this model are described by different conflict scenarios. 
The state 0 represents 0 conflicts, a state where all flits are forwarded. 
The state 1 represents one conflict, a state where two of the four flits are destined in the same direction, and the other two do not conflict.
The state 2 represents where two of the flits are in conflct with eachother, and the other two flits are also in conflict.
The state 3 represents where three of the flits are in conflict with eachother.

A channel in the router cannot have a flit forwarded to itself, meaning that all four flits in the model cannot conflict with eachother.

The transition probabilities for the abstract model are calculated by defining the four state in the modest concrete model. The concrete model is then run for two clock cycles. Properties in the Modest model are defined to find the probabilities of transitioning between states in the four state model.

This gives us the following model:

	to
from	0	1	2	3
0	1/9	16/27	4/27	4/27
1	1/9	16/27	4/27	4/27
2	5/36	11/18	5/36	1/9
3	0	4/9	2/9	1/3

# Counter example generation

We then create counter examples to this abstract model. To do this, we created a python script that runs the concrete model and compares it to the abstract model. The concrete model has 81 different starting configurations. The script runs the concrete model 81 times, once for each starting state, for one clock cycle. The model then get the probabilities for wach state transition and comapres it to the probabilities from the abstract model. If there is a discrepancy, the state and is reported as a counter example.

# Abstract model generation

We then create a new abstract model by adding the counter examples created in the counter example generation to the previous model. We do this by combining counter examples that have the same concrete transition probabilities into a clause. These clauses are added to the model as predicates. A predicate is added to the model by taking the union of each of the states in the model and the predicate, as well as the union of each state and the inverse of the predicate. This is seen in the example below.

# Example
The states of the four state model are defined below.

S0 (0)	- 1230 || 1302 || 1032 || 2301 || 2310 || 2031 || 3012 || 3201 || 3210
S1 (1)	- 1231 || 1232 || 1200 || 1201 || 1202 || 1210 || 1300 || 1310 || 1312 || 1330 || 1332 || 1031 || 1012 || 1030 || 1002 || 2230 || 2231 || 2201 || 2210 || 2300 || 2311 || 2302 || 2312 || 2011 || 2030 || 2001 || 2010 || 3211 || 3230 || 3231 || 3202 || 3212 || 3200 || 3301 || 3302 || 3310 || 3312 || 3011 || 3031 || 3032 || 3001 || 3002 || 3010
S2 (2)	- 2332 || 3232 || 3311 || 1001 || 1010 || 2200 || 1212 || 1331 || 2211 || 2002 || 3300 || 3030
S3 (3)	- 1000 || 2000 || 3000 || 1211 || 1311 || 1011 || 2232 || 2202 || 2212 || 3330 || 3331 || 3332

A set of the counter examples generated from the previous model are shown below.

1212->0	Abstract probability: 0.1388888888888889	Concrete probability: 0.111111111111111	Difference: 0.0277777777777779
1212->1	Abstract probability: 0.6111111111111112	Concrete probability: 0.666666666666667	Difference: -0.0555555555555558
1212->2	Abstract probability: 0.1388888888888889	Concrete probability: 0.111111111111111	Difference: 0.0277777777777779

1331->0	Abstract probability: 0.1388888888888889	Concrete probability: 0.111111111111111	Difference: 0.0277777777777779
1331->1	Abstract probability: 0.6111111111111112	Concrete probability: 0.666666666666667	Difference: -0.0555555555555558
1331->2	Abstract probability: 0.1388888888888889	Concrete probability: 0.111111111111111	Difference: 0.0277777777777779

1001->0	Abstract probability: 0.1388888888888889	Concrete probability: 0.222222222222222	Difference: -0.08333333333333309
1001->1	Abstract probability: 0.6111111111111112	Concrete probability: 0.666666666666667	Difference: -0.0555555555555558
1001->2	Abstract probability: 0.1388888888888889	Concrete probability: 0.111111111111111	Difference: 0.0277777777777779
1001->3	Abstract probability: 0.1111111111111111	Concrete probability: 0	Difference: 0.1111111111111111

We generate the predicates by taking the starting state of each counter example, in this case 1212, 1331, and 1001. We combine starting states that have the same concrete transition probabilities into one clause to create a predicate. In this example, 1212, and 1331 have the same concrete transition probabilities, so they would be combined into a clause 1212 || 1331. 1001 is not included because the state has different contrete transition probabilities.

The predicate 1212 || 1331 is added in the following way, generating new states:

S0 && (1212 || 1331) := False
S0 && !(1212 || 1331) := S0

S1 && (1212 || 1331) := False
S1 && !(1212 || 1331) := S1

S2 && (1212 || 1331) := 1212 || 1331
S2 && !(1212 || 1331) := 2332 || 3232 || 3311 || 1001 || 1010 || 2200 || 2211 || 2002 || 3300 || 3030


S3 && (1212 || 1331) := False
S3 && !(1212 || 1331) := S3


