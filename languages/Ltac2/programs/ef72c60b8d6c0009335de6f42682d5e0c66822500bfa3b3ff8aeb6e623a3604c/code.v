From Ltac2 Require Import Ltac2.

(** A tactic that proves goals of the form [n = n] *)
Ltac2 solve_refl () :=
  match! goal with
  | [ |- ?x = ?x ] => reflexivity ()
  | [ |- _ ] =>
    Control.zero (Tactic_failure None)
  end.

(** Repeatedly apply a tactic until it fails *)
Ltac2 rec repeat0 (t : unit -> unit) : unit :=
  Control.plus (fun () => t (); repeat0 t) (fun _ => ()).

(** Solve universally quantified reflexivity goals *)
Ltac2 solve_forall_refl () :=
  repeat0 (fun () => intro _);
  solve_refl ().

Goal forall (n : nat), n = n.
Proof.
  solve_forall_refl ().
Qed.

Goal forall (s : string), s = s.
Proof.
  solve_forall_refl ().
Qed.
