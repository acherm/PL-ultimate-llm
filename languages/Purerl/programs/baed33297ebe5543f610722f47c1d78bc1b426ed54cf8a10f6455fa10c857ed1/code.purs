module Main where

import Prelude
import Effect (Effect)
import Effect.Console (log)

-- Fibonacci using pattern matching
fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n - 1) + fib (n - 2)

main :: Effect Unit
main = do
  log "Fibonacci sequence:"
  log (show (map fib (0..10)))
