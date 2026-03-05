// Natural numbers
constant symbol Nat : TYPE;
constant symbol zero : Nat;
constant symbol succ : Nat → Nat;

// Addition
symbol add : Nat → Nat → Nat;
rule add zero $n ↪ $n;
rule add (succ $m) $n ↪ succ (add $m $n);

// Multiplication
symbol mul : Nat → Nat → Nat;
rule mul zero $n ↪ zero;
rule mul (succ $m) $n ↪ add (mul $m $n) $n;

// Proofs of basic properties
symbol Eq : Nat → Nat → TYPE;
constant symbol refl : Π x, Eq x x;
symbol eq_sym : Π x y, Eq x y → Eq y x;
rule eq_sym _ _ (refl _) ↪ refl _;

// add_zero: add n zero = n
symbol add_zero : Π n, Eq (add n zero) n;
rule add_zero zero ↪ refl zero;
rule add_zero (succ $n) ↪ refl (succ (add $n zero));
