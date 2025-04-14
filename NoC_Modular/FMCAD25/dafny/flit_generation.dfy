include "flit.dfy"

method discrete_uniform(min: int, max: int) returns (val: int)
  requires min <= max 
  ensures {:axiom} min <= val <= max

method generate_flits<T(0)>(this_id: nat, max_id: nat, payload: T) returns (f: Flit)
  requires 0 <= this_id <= max_id
  requires 1 <= max_id
  ensures f.destination.Id?
  ensures 0 <= f.destination.id <= max_id && f.destination.id != this_id
{
  var destination := discrete_uniform(0, max_id - 1);

  var dest := if destination >= this_id 
       then destination + 1 
       else destination;
  
  f := Flit(Id(dest), payload);

  return f;
}