(* Prove that addition is commutative for natural numbers *)
needs "arith.ml";;

let ADD_COMM = prove
 (`!m n. m + n = n + m`,
  REPEAT GEN_TAC THEN
  SPEC_TAC (`n:num`,`n:num`) THEN
  INDUCT_TAC THEN
  ASM_REWRITE_TAC[ADD_CLAUSES]);;

(* Prove that 0 is the additive identity *)
let ADD_0 = prove
 (`!n. n + 0 = n`,
  GEN_TAC THEN
  REWRITE_TAC[ADD_CLAUSES]);;
