let rec fact = fun n -> if n = 0 then 1 else n * (fact (n - 1))

let rec fib = fun n ->
  if n = 0 then 0
  else if n = 1 then 1
  else (fib (n - 1)) + (fib (n - 2))

let main =
  let f = fact 10 in
  let g = fib 10 in
  (f, g)
