-- Parallel Fibonacci using pH
module Fib where

fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = f1 `par` (f2 `seq` (f1 + f2))
  where
    f1 = fib (n-1)
    f2 = fib (n-2)

main = print (fib 10)
