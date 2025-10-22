Inductive nat : Set := O : nat | S : nat -> nat.

Definition plus (n m : nat) : nat :=
  match n with
  | O => m
  | S p => S (plus p m)
  end.

Lemma plus_O_n : forall n : nat, plus O n = n.
Proof.
  intro n.
  reflexivity.
Qed.

Lemma plus_S_n : forall n m : nat, plus (S n) m = S (plus n m).
Proof.
  intros n m.
  reflexivity.
Qed.

Lemma plus_comm : forall n m : nat, plus n m = plus m n.
Proof.
  intros n m.
  induction n as [| n' IHn'].
  - simpl. rewrite plus_O_n. reflexivity.
  - simpl. rewrite IHn'. rewrite plus_S_n. reflexivity.
Qed.