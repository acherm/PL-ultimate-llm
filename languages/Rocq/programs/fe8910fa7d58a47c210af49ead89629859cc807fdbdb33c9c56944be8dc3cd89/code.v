Require Import Coq.Arith.Arith.

Fixpoint factorial (n : nat) : nat :=
  match n with
  | O => 1
  | S n' => n * factorial n'
  end.

Theorem factorial_positive : forall n : nat,
  factorial n > 0.
Proof.
  intros n.
  induction n as [| n' IHn'].
  - simpl. omega.
  - simpl. apply Nat.mul_pos_pos.
    + omega.
    + exact IHn'.
Qed.