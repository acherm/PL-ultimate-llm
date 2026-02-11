module Main

import Data.Vect

bottles : Nat -> String
bottles Z = "no more bottles"
bottles (S Z) = "1 bottle"
bottles (S (S k)) = show (S (S k)) ++ " bottles"

verse : Nat -> String
verse Z = "No more bottles of beer on the wall, no more bottles of beer.\nGo to the store and buy some more, 99 bottles of beer on the wall."
verse (S k) = bottles (S k) ++ " of beer on the wall, " ++ bottles (S k) ++ " of beer.\nTake one down, pass it around, " ++ bottles k ++ " of beer on the wall."

main : IO ()
main = putStrLn (unlines (map verse [0..99]))