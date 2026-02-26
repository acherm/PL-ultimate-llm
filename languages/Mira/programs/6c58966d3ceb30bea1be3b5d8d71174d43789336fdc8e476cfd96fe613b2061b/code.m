qsort [] = []
qsort (a:x) = qsort [b | b <- x; b<=a] ++ [a] ++ qsort [b | b <- x; b>a]

main = show (qsort [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
