-- Length function in Omega
data Nat = Zero | Succ Nat

length :: forall (a :: *) . [a] -> Nat
length [] = Zero
length (x:xs) = Succ (length xs)

-- Example usage
main = length [1, 2, 3, 4, 5]
