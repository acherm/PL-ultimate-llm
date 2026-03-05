Fixpoint fib (n : nat) : nat :=
  match n with
  | O => O
  | S O => S O
  | S (S n' as m) => fib n' + fib m
  end.
