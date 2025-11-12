# Old Models

These are models that were part of the process of generating a working model while
writing the paper for FMCAD. Notes about each model are given below.

- [flit_generation](./flit_generation.modest): This model was an abstraction of our flit
  generation process that we used to verify that our flit generation process was correct.
  Because when we started this work initially we had issues with state space explosion we
  thought that we would have to separate out all of the processes in our model and verify
  them individually. Luckily, that didn't end up being the case but
  [this](./flit_generation.modest) file is an artifact of that research.
- [functional_verification_abstract](./functional_verification_abstract.modest): This was
  our initial attempt at creating an abstracted central router that could model all
  possible behavior of the NoC. We abstracted the behavior for every router to be a basic
  sender/receiver, except for we modelled the entire behavior of the central router. This
  model had issues that were inherent in our earlier design including the unfortunate
  habit of needing several thousand gigabytes to represent the state space. We were able
  to resolve this with later models.
- [modular_functional_verification](./modular_functional_verification.modest): This model
  was the original attempt to verify the correctness of the modular NoC design using PCTL
  properties (before Modest support CTL). This model was not optimized in any way, and
  thus did not have a reasonable state space.
- [optimized](./optimized.modest): This was the first model that we were able to use
  `action`s in Modest to model the synchronous behavior of the NoC. We realized that
  Modest was considering many different interleavings that we didn't actually care
  about, so we inserted synchronizing actions so the model acted synchronously.
