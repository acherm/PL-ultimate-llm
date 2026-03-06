(* Ltac: Coq's built-in tactic definition language *)
(* Demonstrates recursive tactics and goal matching *)

Require Import Arith.

(* A recursive tactic using pattern matching *)
Ltac nat_iter n tac :=
  match n with
  | O => idtac
  | S ?n' => tac; nat_iter n' tac
  end.

(* A tactic that matches the proof goal *)
Ltac solve_simple_eq :=
  match goal with
  | |- ?n = ?n           => reflexivity
  | |- 0 + ?n = ?n       => simpl; reflexivity
  | |- ?n + 0 = ?n       => rewrite Nat.add_0_r; reflexivity
  | |- S ?n = S ?m       => f_equal; solve_simple_eq
  end.

(* Tactic that searches hypotheses for False *)
Ltac elim_false :=
  match goal with
  | H : False |- _ => destruct H
  end.

Lemma add_n_0 : forall n, n + 0 = n.
Proof.
  intro n. solve_simple_eq.
Qed.

Lemma add_0_n : forall n, 0 + n = n.
Proof.
  intro n. solve_simple_eq.
Qed.

Lemma succ_inj_eq : forall n, S n = S n.
Proof.
  intro n. solve_simple_eq.
Qed.
