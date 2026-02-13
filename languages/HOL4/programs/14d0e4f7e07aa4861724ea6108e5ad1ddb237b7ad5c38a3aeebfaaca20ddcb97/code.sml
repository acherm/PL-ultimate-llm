(* Simple proof in HOL4: commutativity of addition *)

open HolKernel boolLib Parse bossLib arithmeticTheory;

val _ = new_theory "addition_comm";

(* Prove that addition is commutative *)
val ADD_COMM_THM = store_thm(
  "ADD_COMM_THM",
  ``!m n. m + n = n + m``,
  Induct THEN ASM_REWRITE_TAC[ADD_CLAUSES]
);

val _ = export_theory();
