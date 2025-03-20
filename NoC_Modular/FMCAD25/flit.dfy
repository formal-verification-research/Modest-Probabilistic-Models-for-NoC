// `T` represents the payload of the flit.
class Flit {
  const destination: nat

  constructor(destination: nat)
  {
    this.destination := destination;
  }

  function getDestinationChannel(): nat
    reads this 
  {
    this.destination
  }
}