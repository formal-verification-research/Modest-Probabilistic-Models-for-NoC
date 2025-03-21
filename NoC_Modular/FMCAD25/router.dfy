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
  {
    // ensures all "channel"-related array lengths are 5, as there are 
    // 5 channels out of the router
    && priority_list.Length == 5
    && channels.Length == 5
    && used.Length == 5
    // Ensure every element in the priority list is always unique
    && (forall i: nat, j: nat :: 
        && i < priority_list.Length 
        && j < priority_list.Length 
        && i != j 
        && priority_list[i] != priority_list[j])
  }

}