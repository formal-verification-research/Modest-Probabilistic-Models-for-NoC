include "id.dfy"

// Originally, Flit was parameterized over `T`, where 
// `T` represents the payload of the flit. However, I ran 
// into issues with that so I removed it for the time 
// being
datatype Flit = Flit(destination: Id)