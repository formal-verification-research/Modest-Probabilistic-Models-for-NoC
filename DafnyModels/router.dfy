// include "flit_generation.dfy"
include "channel.dfy"
include "neighbor.dfy"

method discrete_uniform(min: int, max: int) returns (val: int)
  requires min <= max 
  ensures {:axiom} min <= val <= max

method generate_flits(this_id: nat, max_id: nat) returns (f: Flit)
  requires 0 <= this_id <= max_id
  requires 1 <= max_id
  ensures f.destination.Id?
  ensures 0 <= f.destination.id <= max_id && f.destination.id != this_id
{
  var destination := discrete_uniform(0, max_id - 1);

  var dest := if destination >= this_id 
       then destination + 1 
       else destination;
  
  f := Flit(Id(dest));

  return f;
}

class Router {
  const ids: array<Id>
  const id: Id
  var channels: array<Channel>
  var priority_list: array<Neighbor>
  var serviced: nat 
  var unserviced: nat 
  var total_unserviced: nat
  var this_activity: nat
  var last_activity: nat
  var used: array<bool>

  ghost predicate Valid()
    reads this
    reads priority_list
    reads ids
  {
    && this.id.Id?
    // ensures all "channel"-related array lengths are 5, as there are 
    // 5 channels out of the router
    && priority_list.Length == 5
    && channels.Length == 5
    && used.Length == 5
    && this.ids.Length == 4
    // Ensure every element in the priority list is always unique
    && (forall i: nat, j: nat :: 
        (&& 0 <= i < priority_list.Length
         && 0 <= j < priority_list.Length 
         && i != j)
        ==> priority_list[i] != priority_list[j])
    // Ensures all destination id's are unique (or NC)
    && (forall i, j :: 
        (&& 0 <= i < this.ids.Length
         && 0 <= j < this.ids.Length
         && i != j)
        ==> (|| ids[i] != ids[j]
             || ids[i] == NoConnect 
             || ids[j] == NoConnect))
  }

  constructor (buffer_capacity: nat, id: Id, ids: seq<Id>)
    requires buffer_capacity > 0
    requires |ids| == 4
    requires id.Id?
    requires forall i, j :: 
        (&& 0 <= i < |ids|
         && 0 <= j < |ids|
         && i != j)
        ==> (|| ids[i] != ids[j]
             || ids[i] == NoConnect 
             || ids[j] == NoConnect)
    ensures Valid()
    ensures this.id == id
    ensures this_activity == 0
    ensures last_activity == 0
    ensures forall i | 0 <= i < |ids| :: this.ids[i] == ids[i]
    ensures priority_list[..] == [North, East, South, West, Local]
    ensures used[..] == [false, false, false, false, false]
    ensures channels.Length == 5
    ensures forall c :: c in channels[..] ==> (c.isEmpty() && !c.isServiced())
  {
    this.id := id;
    this.ids := new Id[ |ids| ](i requires 0 <= i < |ids| => ids[i]);

    this.this_activity := 0;
    this.last_activity := 0;

    var default_channel := new Channel(buffer_capacity);
    this.channels := new Channel[5](_ => default_channel);

    this.priority_list := new Neighbor[5][North, East, South, West, Local];

    this.used := new bool[5][false, false, false, false, false];
  }

  method generateFlits(clk: nat)
    requires Valid()
    modifies this
    modifies this.channels
    ensures Valid() 
  {
    if (clk % 10 < 3 && !this.channels[LOCAL].isFull()) {

      assume {:axiom} this.id.id <= this.ids.Length;
      var flit := generate_flits(this.id.id, this.ids.Length);
      this.channels[LOCAL].insert(flit);
    }
  }


  method advanceRouter()
    requires Valid()
    ensures Valid() 
  {
    for id := 0 to this.ids.Length
    {
      advanceChannel(id);
    }
  }

  method advanceChannel(id: nat)
    requires Valid()
    requires 0 <= id < ids.Length
    ensures Valid()
  {
    if (this.ids[id] == NoConnect) {
      return;
    }
  }


}