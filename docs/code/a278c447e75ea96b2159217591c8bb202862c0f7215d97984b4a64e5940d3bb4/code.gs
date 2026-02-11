-- Factorial function in Gofer
factorial :: Int -> Int
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- Main computation
main = do
    print (factorial 5)
    print (factorial 10)
