include "buffer.dfy"

class Channel {
  var buffers: Buffer
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

  method service()
    requires Valid()
    requires !this.isServiced()
    requires !this.buffers.isEmpty()
    modifies this
    modifies this.buffers
    ensures this.buffers.size < old(this.buffers.size)
    ensures this.isServiced()
    ensures Valid()
  {
    this.serviced := true;
    this.buffers.extract();
  }
}