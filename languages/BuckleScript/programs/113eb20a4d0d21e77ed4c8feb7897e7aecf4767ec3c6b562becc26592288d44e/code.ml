(* Fibonacci sequence in BuckleScript *)
let rec fib n =
  if n <= 1 then n
  else fib (n - 1) + fib (n - 2)

let () =
  for i = 0 to 10 do
    Js.log (string_of_int (fib i))
  done
