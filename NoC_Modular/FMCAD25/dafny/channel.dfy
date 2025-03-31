include "buffer.dfy"

class Channel<T(0,==)> {
  var buffers: Buffer<T>
  var serviced: bool

  ghost predicate Valid()
    reads this 
    reads this.buffers
  {
    && this.buffers.Valid()
  }

  constructor(capacity: nat)
    requires capacity > 0
    ensures Valid()
    ensures this.isServiced() == false
    ensures this.isEmpty() == true
    ensures this.isFull() == false
  {
    this.buffers := new Buffer(capacity);
    this.serviced := false;
  }

  predicate isFull()
    reads this
    reads this.buffers
  {
    buffers.isFull()
  }

  predicate isEmpty()
    reads this
    reads this.buffers
  {
    buffers.isEmpty()
  }

  // Give a nice symmetric API to the channel class. Now all 
  // predicates can be checked with function calls like this:
  // channel.is<Variable>()
  predicate isServiced()
    reads this 
  {
    serviced
  }

  method insert(f: Flit<T>)
    requires Valid()
    requires !this.buffers.isFull()
    modifies this
    modifies this.buffers 
    modifies this.buffers.flits
    ensures Valid()
    ensures this.buffers.size > old(this.buffers.size)
    ensures f == this.buffers.peekFront()
  {
    this.buffers.insert(f);
  }

  method extract() returns (f: Flit<T>)
    requires Valid()
    requires !this.isServiced()
    requires !this.buffers.isEmpty()
    modifies this
    modifies this.buffers
    modifies this.buffers.flits
    ensures Valid()
    ensures this.buffers.size < old(this.buffers.size)
    ensures f == old(this.buffers.peekBack())
    ensures this.isServiced()
  {
    this.serviced := true;
    f := this.buffers.extract();
  }

  method resetServiced()
    requires Valid()
    modifies this
    ensures Valid() 
    ensures !this.isServiced()
  {
    this.serviced := false;
  }
}