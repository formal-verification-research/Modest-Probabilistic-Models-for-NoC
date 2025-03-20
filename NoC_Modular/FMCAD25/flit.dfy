// `T` represents the payload of the flit.
datatype Flit<T(0,==)> = Flit(destination: nat, payload: T)