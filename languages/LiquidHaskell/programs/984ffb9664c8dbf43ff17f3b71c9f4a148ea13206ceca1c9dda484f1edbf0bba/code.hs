module Main where

{-@ type Nat = {v:Int | v >= 0} @-}

{-@ fibonacci :: Nat -> Nat @-}
fibonacci :: Int -> Int
fibonacci 0 = 0
fibonacci 1 = 1
fibonacci n = fibonacci (n-1) + fibonacci (n-2)

{-@ abs' :: Int -> Nat @-}
abs' :: Int -> Int
abs' n
  | n < 0    = (-n)
  | otherwise = n

main :: IO ()
main = do
  putStrLn "Fibonacci sequence:"
  mapM_ (print . fibonacci) [0..10]
  putStrLn "Absolute values:"
  mapM_ (\x -> print (abs' x)) [-3..3]
