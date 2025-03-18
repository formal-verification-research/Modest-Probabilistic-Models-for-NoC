class Buffer {
  const capacity: nat
  var size: nat
  var head: nat
  var tail: nat

  ghost predicate Valid()
    reads this
  {
    && size <= capacity
    && head < capacity
    && tail < capacity
    && (head == tail ==> (size == 0 || size == capacity))
    && (head > tail ==> head - tail == size)
    && (head < tail ==> (head + capacity) - tail == size)
  }

  constructor(capacity: int)
    requires capacity > 0
    ensures Valid()
  {
    this.capacity := capacity;
    this.size := 0;
    this.head := 0;
    this.tail := 0;
  }

  method insert()
    requires Valid() && size < capacity
    modifies this
    ensures Valid()
  {
    size := size + 1;
    head := if head >= capacity - 1 then 0 else head + 1;
  }

  method extract()
    requires Valid() && size > 0
    modifies this
    ensures Valid()
  {
    size := size - 1;
    tail := if tail >= capacity - 1 then 0 else tail + 1;
  }
}
