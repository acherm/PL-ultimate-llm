type storage = int

type result = operation list * storage

[@entry]
let increment (n : int) (store : storage) : result =
  [], store + n

[@entry]
let decrement (n : int) (store : storage) : result =
  [], store - n

[@entry]
let reset (() : unit) (_store : storage) : result =
  [], 0
