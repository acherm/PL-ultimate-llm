module Main

fibonacci : Nat -> Nat
fibonacci Z = Z
fibonacci (S Z) = S Z
fibonacci (S (S k)) = fibonacci (S k) + fibonacci k

main : IO ()
main = do
  putStrLn "Fibonacci numbers:"
  printLn (fibonacci 0)
  printLn (fibonacci 1)
  printLn (fibonacci 5)
  printLn (fibonacci 10)
