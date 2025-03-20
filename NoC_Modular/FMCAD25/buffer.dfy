include "flit.dfy"

class Buffer<T(0,==)> {
  const capacity: nat
  var size: nat
  var head: nat
  var tail: nat
  var flits: array<Flit<T>>

  ghost predicate Valid()
    reads this
  {
    && size <= capacity
    && head < capacity
    && tail < capacity
    && (head == tail ==> (size == 0 || size == capacity))
    && (head > tail ==> head - tail == size)
    && (head < tail ==> (head + capacity) - tail == size)
    && flits.Length == capacity
  }

  constructor(capacity: int)
    requires capacity > 0
    ensures Valid()
  {
    this.capacity := capacity;
    this.size := 0;
    this.head := 0;
    this.tail := 0;
    this.flits := new Flit[capacity];
  }

  method insert(payload: Flit<T>)
    requires Valid() && size < capacity
    modifies this
    modifies this.flits
    ensures Valid()
    ensures size > old(size)
    ensures this.flits[old(head)] == payload
  {
    // insert the flit
    this.flits[head] := payload;

    // update the size and increment the head position
    size := size + 1;
    head := if head >= capacity - 1 then 0 else head + 1;
  }

  method extract() returns (f: Flit<T>)
    requires Valid() && size > 0
    modifies this
    modifies this.flits
    ensures Valid()
    ensures size < old(size)
    ensures f == this.flits[old(tail)]
  {
    // extract the value
    f := this.flits[tail];

    // update the size and move the tail pointer
    size := size - 1;
    tail := if tail >= capacity - 1 then 0 else tail + 1;
  }

  predicate isFull()
    reads this
  {
    size == capacity
  }

  predicate isEmpty()
    reads this
  {
    size == 0
  }

}
