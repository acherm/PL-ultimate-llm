{-@ LIQUID "--no-termination" @-}
module SafeOps where

{-@ type Pos = {v:Int | v > 0} @-}
{-@ type NonEmpty a = {v:[a] | len v > 0} @-}

{-@ head' :: NonEmpty a -> a @-}
head' :: [a] -> a
head' (x:_) = x
head' []    = error "unreachable"

{-@ safeDiv :: Int -> {v:Int | v /= 0} -> Int @-}
safeDiv :: Int -> Int -> Int
safeDiv x y = x `div` y

{-@ factorial :: Nat -> Pos @-}
factorial :: Int -> Int
factorial 0 = 1
factorial n = n * factorial (n - 1)

main :: IO ()
main = do
    let xs = [1, 2, 3] :: [Int]
    putStrLn $ "Head: "    ++ show (head' xs)
    putStrLn $ "10 / 2 = " ++ show (safeDiv 10 2)
    putStrLn $ "5! = "     ++ show (factorial 5)
