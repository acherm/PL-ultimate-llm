(* CameLIGO counter smart contract *)
type storage = int

type parameter =
  | Increment of int
  | Decrement of int
  | Reset

type return = operation list * storage

let add (store : storage) (delta : int) : storage = store + delta

let sub (store : storage) (delta : int) : storage = store - delta

let main (action : parameter) (store : storage) : return =
  let new_store : storage =
    match action with
    | Increment n -> add store n
    | Decrement n -> sub store n
    | Reset       -> 0
  in
  ([] : operation list), new_store
