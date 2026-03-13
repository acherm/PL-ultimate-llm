module Factorial

val factorial : n:nat -> Tot nat
let rec factorial n =
  if n = 0 then 1
  else n * factorial (n - 1)

let main () : FStar.All.ML unit =
  let result = factorial 10 in
  FStar.IO.print_string ("10! = " ^ string_of_int result ^ "\n")
