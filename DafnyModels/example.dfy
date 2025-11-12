datatype ClockEvent = 
  | RisingEdge
  | FallingEdge

class DFF {
  var bit: bv1

  constructor()
  {
    bit := 0;
  }

  method onRisingEdge(value: bv1)
    modifies this
    ensures this.bit == value
  {
    this.bit := value;
  }
}

class Clock {
  var value: bv1

  constructor()
  {
    value := 0;
  }

  method toggle() returns (event: ClockEvent)
    modifies this
    ensures (old(this.value) == 1) ==> this.value == 0
    ensures (old(this.value) == 0) ==> this.value == 1
  {
    if (this.value == 1) {
      this.value := 0;
      event := FallingEdge;
    } else {
      this.value := 1;
      event := RisingEdge;
    }
  }
}

method run(clk: Clock, dff: DFF, input: bv1)
  modifies clk, dff
{
  var event := clk.toggle();
  var old_bit := dff.bit;

  match event {
    case FallingEdge =>
    case RisingEdge => dff.onRisingEdge(input);
  }
}

lemma schedule(clk: Clock, dff: DFF, input: bv1)
  ensures (old(clk.value) == 0 && clk.value == 1) ==> dff.bit == input
  ensures !(old(clk.value) == 0 && clk.value == 1) ==> dff.bit == old(dff.bit)
{
}