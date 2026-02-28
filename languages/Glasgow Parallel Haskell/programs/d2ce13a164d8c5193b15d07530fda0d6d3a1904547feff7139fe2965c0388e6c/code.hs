import Control.Parallel

fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = f1 `par` f2 `pseq` (f1 + f2)
  where
    f1 = fib (n-1)
    f2 = fib (n-2)

main :: IO ()
main = print (fib 34)
