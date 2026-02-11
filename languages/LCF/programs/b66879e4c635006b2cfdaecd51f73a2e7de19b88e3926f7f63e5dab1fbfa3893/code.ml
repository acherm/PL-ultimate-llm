let ADD_COMM = prove
  ("!m n. m + n = n + m",
   INDUCT_TAC THEN ASM_REWRITE_TAC[ADD_CLAUSES]);;

let ADD_ASSOC = prove
  ("!m n p. m + (n + p) = (m + n) + p",
   INDUCT_TAC THEN ASM_REWRITE_TAC[ADD_CLAUSES]);;
