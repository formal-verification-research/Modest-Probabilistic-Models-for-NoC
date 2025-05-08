# TODOs before submission

## Checking

1. Modest check on PCTL PSN
2. Modest check on CTL correctness
3. Modest check on PCTL correctness
4. Re-review Jonah's checks
5. Check clock counter (don't need for correctness)

## More Assume-Guarantee

1. Split out all properties in [functional](./models/modular_functional_verification.modest)
   for AG type reasoning
2. Add a model that abstracts away the network

### AG Model

- Abstract away neighbors into sender/receiver process
- S/R needs to be able to:
  1. send new flits (random dest, random timing)
  2. check if router buffer is full
  3. check if S/R is full

## CTL In Modest

1. Check a small model using `discreteUniformRandom()` with CTL properties
   - Check small models
     - Basic test: passed. [ctl_dist_test.modest](./models/ctl_dist_test.modest)
   - Based off results, email Arnd

## Findings

### Old Model Comparison

Why didn't previous models run into this issue? On further inspection of the models
used to validate the router, I realized that they still had the clock bound in place
of up to 20 cycles. By moving away from using the bounded clocks style found in Jonah's
thesis and instead using reward bounded properties, we effectively remove the upper
limit for clock cycles which in turn must allow for a much larger state space.

Some more research will need to be done as to _why_ this is exactly, but that's my
hypothesis for now.

## To Add to Paper

- BDDs and lists
- Models with fixed size state

## To work on

- Try to look for variables that are not reset after a router is used. My thought is
  that if all the buffers are emptied out after 9 clock cycles, the router should
  basically be in it's initial state, but clearly it isn't. We'll have to see why.
