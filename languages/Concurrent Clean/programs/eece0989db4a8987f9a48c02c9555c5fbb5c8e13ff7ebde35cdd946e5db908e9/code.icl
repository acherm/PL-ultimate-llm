module fib
import StdEnv

fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n-1) + fib (n-2)

Start = map fib [0..10]
