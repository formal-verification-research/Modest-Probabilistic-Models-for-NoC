# List vs Array

## Test

We have an issue with state space explosion, and so I thought to fix it I might try to switch the data structure we use. However, this doesn't appear to really change the state space.

## Results With Single Input Values

The enqueue method looks like this:

```modest
enqueue(1, list) // list
enqueue(arr, 1) // array
```

I created a test where two parallel processes randomly enqueued or dequeued the value of 1 into the array. The results of the test showed that `array` required less states but more memory, and `list` was the opposite.

- Array:

  ```text
  Min. state size:    88 bytes
  States:             4
  ...
  Peak memory:        100.38 MB
  ```

- List:

  ```text
  Min. state size:    32 bytes
  States:             16
  ...
  Peak memory:        44.41 MB
  ```

## Results with DiscreteUniform input values

I changed the enqueue method to look like this:

```modest
enqueue(DiscreteUniform(0, 9), list) // list
enqueue(arr, DiscreteUniform(0, 9)) // array
```

- Array:
  
  ```text
  Min. state size:    88 bytes
  States:             121
  Transitions:        121
  Branches:           4500
  Rate:               644 states/s
  Peak memory:        101.47 MB
  ```

- List:

  ```text
  Min. state size:    32 bytes
  States:             33334
  Transitions:        33334
  Branches:           488885
  Rate:               38227 states/s
  Peak memory:        56.00 MB
  ```

Again, `list` had many more states but used less memory than `array`. This seems to indicate that for larger projects `list` is probably the better datatype to use when representing a FIFO-like data structure.
