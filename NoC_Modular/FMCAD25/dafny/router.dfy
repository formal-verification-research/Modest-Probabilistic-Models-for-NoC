include "channel.dfy"
include "neighbor.dfy"

class Router<T(0,==)> {
  const ids: array<Id>
  var channels: array<Channel<T>>
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

  constructor (buffer_capacity: nat, ids: seq<Id>)
    requires buffer_capacity > 0
    requires |ids| == 4
    requires forall i, j :: 
        (&& 0 <= i < |ids|
         && 0 <= j < |ids|
         && i != j)
        ==> (|| ids[i] != ids[j]
             || ids[i] == NoConnect 
             || ids[j] == NoConnect)
    ensures Valid()
    ensures this_activity == 0
    ensures last_activity == 0
    ensures forall i | 0 <= i < |ids| :: this.ids[i] == ids[i]
    ensures priority_list[..] == [North, East, South, West, Local]
    ensures used[..] == [false, false, false, false, false]
    ensures channels.Length == 5
    ensures forall c :: c in channels[..] ==> (c.isEmpty() && !c.isServiced())
  {
    this.this_activity := 0;
    this.last_activity := 0;

    this.ids := new Id[ |ids| ];
    var default_channel := new Channel<T>(buffer_capacity);
    this.channels := new Channel<T>[5](_ => default_channel);
    this.priority_list := new Neighbor[5][North, East, South, West, Local];
    this.used := new bool[5][false, false, false, false, false];

    new;
    
    forall i | 0 <= i < this.ids.Length { this.ids[i] := ids[i]; }
  }

}