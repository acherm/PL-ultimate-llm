-- Fibonacci sequence in Expresso
-- Expresso is a minimal statically-typed functional scripting language

let rec fib n =
  if n <= 1 then n
  else fib (n - 1) + fib (n - 2)

let results = { fib0 = fib 0
              , fib1 = fib 1
              , fib5 = fib 5
              , fib10 = fib 10
              }

in results
