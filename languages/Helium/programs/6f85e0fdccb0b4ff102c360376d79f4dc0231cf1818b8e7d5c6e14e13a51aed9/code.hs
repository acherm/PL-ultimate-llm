quicksort :: [Int] -> [Int]
quicksort [] = []
quicksort (x:xs) = quicksort smaller ++ [x] ++ quicksort larger
  where
    smaller = [a | a <- xs, a <= x]
    larger = [b | b <- xs, b > x]

main :: IO ()
main = print (quicksort [3, 1, 4, 1, 5, 9, 2, 6])
