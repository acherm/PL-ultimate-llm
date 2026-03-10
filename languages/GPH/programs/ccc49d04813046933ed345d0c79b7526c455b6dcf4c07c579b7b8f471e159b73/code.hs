import Control.Parallel (par, pseq)

-- Parallel Fibonacci using par/pseq
parFib :: Int -> Int
parFib 0 = 0
parFib 1 = 1
parFib n = x `par` y `pseq` (x + y)
  where
    x = parFib (n - 1)
    y = parFib (n - 2)

-- Parallel sum of a list using divide and conquer
parSum :: [Int] -> Int
parSum [] = 0
parSum [x] = x
parSum xs = left `par` right `pseq` (left + right)
  where
    (ls, rs) = splitAt (length xs `div` 2) xs
    left  = parSum ls
    right = parSum rs

main :: IO ()
main = do
    let fibs = map parFib [0..15]
    mapM_ print fibs
    let total = parSum [1..100]
    putStrLn ("Sum 1..100 = " ++ show total)
