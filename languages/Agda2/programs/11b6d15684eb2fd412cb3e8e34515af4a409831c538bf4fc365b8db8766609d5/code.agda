module Fibonacci where

open import Data.Nat using (ℕ; zero; suc; _+_)

-- Fibonacci numbers defined by structural recursion
fib : ℕ → ℕ
fib zero              = zero
fib (suc zero)        = suc zero
fib (suc (suc n))     = fib n + fib (suc n)

-- First ten Fibonacci numbers (unary representation)
fib0  = fib 0
fib1  = fib 1
fib2  = fib 2
fib3  = fib 3
fib4  = fib 4
fib5  = fib 5
fib6  = fib 6
fib7  = fib 7
fib8  = fib 8
fib9  = fib 9
