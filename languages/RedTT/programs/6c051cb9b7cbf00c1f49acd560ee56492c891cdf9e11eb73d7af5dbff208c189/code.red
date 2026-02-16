-- Natural numbers in RedTT
def Nat : type where
| zero
| suc (n : Nat)

-- Addition function
def add (m : Nat) (n : Nat) : Nat where
| zero, n => n
| suc m', n => suc (add m' n)

-- Example: 2 + 1 = 3
def two : Nat where
| => suc (suc zero)

def one : Nat where
| => suc zero

def three : Nat where
| => add two one
