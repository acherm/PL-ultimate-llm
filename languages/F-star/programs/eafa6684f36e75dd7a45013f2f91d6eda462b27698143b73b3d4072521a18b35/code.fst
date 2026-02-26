module Fibonacci

open FStar.IO

let rec fib (n:nat) : nat =
  match n with
  | 0 -> 0
  | 1 -> 1
  | _ -> fib (n-1) + fib (n-2)

let rec print_fibs (i:nat) (limit:nat) : ML unit =
  if i < limit then begin
    print_string ("fib(" ^ string_of_int i ^ ") = " ^ string_of_int (fib i) ^ "\n");
    print_fibs (i+1) limit
  end

let main () : ML unit =
  print_fibs 0 10
