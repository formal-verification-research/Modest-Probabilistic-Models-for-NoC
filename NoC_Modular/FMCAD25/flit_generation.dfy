type Flit(==) = nat

method discrete_uniform(min: int, max: int) returns (val: int)
  requires min <= max 
  ensures {:axiom} min <= val <= max

method generate_flits(this_id: nat, max_id: nat) returns (f: Flit)
  requires 0 <= this_id <= max_id
  requires 1 <= max_id
  ensures 0 <= f <= max_id && f != this_id
{
  var destination := discrete_uniform(0, max_id - 1);

  f := if destination >= this_id 
       then destination + 1 
       else destination;
  
  return f;
}