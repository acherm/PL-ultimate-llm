module Main exposing (..)

fibonacci : Int -> Int
fibonacci n =
    case n of
        0 -> 0
        1 -> 1
        _ -> fibonacci (n - 1) + fibonacci (n - 2)

main : Int
main =
    fibonacci 10
