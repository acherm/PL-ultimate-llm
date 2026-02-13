-- Natural numbers in Narya
def Nat : Type where
  | zero : Nat
  | succ : Nat → Nat

-- Addition function
def add (m n : Nat) : Nat where
  | zero    , n => n
  | succ m' , n => succ (add m' n)

-- Example: 2 + 3
def two : Nat := succ (succ zero)
def three : Nat := succ (succ (succ zero))
def five : Nat := add two three
