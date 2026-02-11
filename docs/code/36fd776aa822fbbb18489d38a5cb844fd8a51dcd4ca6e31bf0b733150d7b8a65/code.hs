module Problems where

-- Problem 1
myLast :: [a] -> a
myLast [x] = x
myLast (_:xs) = myLast xs