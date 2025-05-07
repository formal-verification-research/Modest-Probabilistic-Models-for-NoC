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
