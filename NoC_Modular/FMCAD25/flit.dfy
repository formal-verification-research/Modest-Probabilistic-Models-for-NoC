include "id.dfy"

// `T` represents the payload of the flit.
datatype Flit<T(0,==)> = Flit(destination: Id, payload: T)