# Statespace Tests

For the FMCAD 25 paper, we experienced issues with state space explosion when trying
to verify the NoC for an unbounded amount of clock cycles. These test models aim to
explain why that is.

## Models

- [Local buffer](./local_buffer.modest): this models a local buffer for up to $N$
  clock cycles.
