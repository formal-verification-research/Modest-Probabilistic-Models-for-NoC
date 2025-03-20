// `T` represents the payload of the flit.
class Flit<T> {
  const destination: nat
  const payload: T 

  constructor(destination: nat, payload: T)
  {
    this.destination := destination;
    this.payload := payload;
  }

  function getDestinationChannel(): nat
    reads this 
  {
    this.destination
  }
}