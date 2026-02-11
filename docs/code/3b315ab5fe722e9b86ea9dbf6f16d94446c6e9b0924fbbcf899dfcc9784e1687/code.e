data Nat : * where
  zero : Nat
  succ : Nat -> Nat

plus : Nat -> Nat -> Nat
plus zero n = n
plus (succ m) n = succ (plus m n)

main : Nat
main = plus (succ (succ zero)) (succ zero)
