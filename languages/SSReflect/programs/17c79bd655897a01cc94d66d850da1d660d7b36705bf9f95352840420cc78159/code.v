From mathcomp Require Import all_ssreflect.
Set Implicit Arguments.
Unset Strict Implicit.
Unset Printing Implicit Defensive.

(* Fibonacci sequence using SSReflect *)
Fixpoint fib (n : nat) : nat :=
  match n with
  | 0 => 0
  | 1 => 1
  | S (S n as m) => fib m + fib n
  end.

Lemma fib0 : fib 0 = 0. Proof. by []. Qed.
Lemma fib1 : fib 1 = 1. Proof. by []. Qed.

Lemma fib_pos n : 0 < fib n.+1.
Proof.
elim: n => [|n IHn] //.
rewrite /= -addn1 -addn1.
by apply leq_add.
Qed.

Lemma fib_sum n : fib n + fib n.+1 = fib n.+2.
Proof. by rewrite /= addnC. Qed.
