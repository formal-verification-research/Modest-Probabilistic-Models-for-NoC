include "flit_generation.dfy"

class X {
  method test() returns (x: Flit) {
    x := generate_flits(2, 10);
  }
}