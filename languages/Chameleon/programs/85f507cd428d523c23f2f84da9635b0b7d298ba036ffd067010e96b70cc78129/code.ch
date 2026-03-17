module Main where

fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n-1) + fib (n-2)

main :: IO ()
main = do
    putStrLn "Fibonacci numbers:"
    mapM_ (putStrLn . show) (map fib [0..10])
