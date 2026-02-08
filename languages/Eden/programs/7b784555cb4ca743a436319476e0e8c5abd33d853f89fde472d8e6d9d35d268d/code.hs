module Main where

import Eden

fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n-1) + fib (n-2)

parfib :: Int -> Int
parfib n | n < 25 = fib n
parfib n = force (pf1 `par` pf2 `par` (pf1 + pf2))
  where pf1 = parfib (n-1)
        pf2 = parfib (n-2)

main :: IO ()
main = print (parfib 35)
