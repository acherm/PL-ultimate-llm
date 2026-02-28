This module demonstrates Literate Haskell using the bird-track convention.
Lines beginning with '>' are executable Haskell; all other lines are prose.

> module Main where
>
> -- | Compute the nth Fibonacci number.
> fib :: Int -> Int
> fib 0 = 0
> fib 1 = 1
> fib n = fib (n - 1) + fib (n - 2)
>
> main :: IO ()
> main = mapM_ print [ fib n | n <- [0..9] ]
