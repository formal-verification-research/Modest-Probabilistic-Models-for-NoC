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
    // Ensure every element in the priority list is always unique
    && (forall i: nat, j: nat :: 
        && 0 < i < priority_list.Length 
        && 0 < j < priority_list.Length 
        && i != j 
        && priority_list[i] != priority_list[j])
    // Ensures all destination id's are unique (or NC)
    && (forall id1, id2 :: 
        && id1 in ids[..]
        && id2 in ids[..]
        && (id1 != id2 || id1 == NoConnect || id2 == NoConnect))
  }

  constructor (buffer_capacity: nat, ids: seq<Id>)
    requires buffer_capacity > 0
    requires |ids| > 0
    requires forall id1, id2 :: 
        && id1 in ids
        && id2 in ids
        && (id1 != id2 || id1 == NoConnect || id2 == NoConnect)
    ensures Valid()
  {
    this.ids := new Id[ |ids| ];
    var default_channel := new Channel<T>(buffer_capacity);
    this.channels := new Channel<T>[5](_ => default_channel);
    this.priority_list := new Neighbor[5];
    this.used := new bool[5](_ => false);

    new; // tbh not sure why I need this

    forall i | 0 <= i < this.ids.Length { this.ids[i] := ids[i]; }

    this.priority_list[0] := North;
    this.priority_list[1] := East;
    this.priority_list[2] := South;
    this.priority_list[3] := West;
    this.priority_list[4] := Local;

    assert priority_list[0] != priority_list[1];
    assert priority_list[0] != priority_list[2];
    assert priority_list[0] != priority_list[3];
    assert priority_list[0] != priority_list[4];
    assert priority_list[1] != priority_list[2];
    assert priority_list[1] != priority_list[3];
    assert priority_list[1] != priority_list[4];
    assert priority_list[2] != priority_list[3];
    assert priority_list[2] != priority_list[4];
    assert priority_list[3] != priority_list[4];
  }

}