(* Simple HOL theorem: commutativity of addition *)
load "arithmeticTheory";
open arithmeticTheory;

val ADD_COMM_THM = store_thm(
  "ADD_COMM_THM",
  ``!m n. m + n = n + m``,
  REWRITE_TAC [ADD_COMM]
);

(* Prove a simple property about multiplication *)
val MULT_BY_ZERO = store_thm(
  "MULT_BY_ZERO",
  ``!n. n * 0 = 0``,
  INDUCT_TAC THEN REWRITE_TAC [MULT_CLAUSES]
);