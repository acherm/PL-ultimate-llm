(* Simple Lens example - bidirectional get/put *)
let swap : (string * string) <-> (string * string) =
  lens snd <-> fst
  in fun (x, y) -> (y, x)

(* Test the lens *)
let result = swap.get ("hello", "world")
