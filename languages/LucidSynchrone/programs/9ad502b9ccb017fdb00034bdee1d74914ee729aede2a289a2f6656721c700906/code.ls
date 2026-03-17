(* LucidSynchrone: edge detector and counter example *)
(* Synchronous reactive programming in ML-like syntax *)

(* detect a rising edge of a boolean signal *)
let node edge (b : bool) : bool =
  b && not (false -> pre b)

(* count the number of true values seen so far *)
let node count (x : bool) : int =
  let rec n = if x then (0 -> pre n) + 1 else (0 -> pre n) in
  n

(* a simple period-n clock: true every n steps *)
let node clock (n : int) : bool =
  let rec c = 0 -> (pre c + 1) mod n in
  c = 0
