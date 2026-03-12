; LISP 1 - Symbolic differentiation
; Based on McCarthy's 1960 paper "Recursive Functions of Symbolic Expressions"
; Originally implemented on the IBM 704, 1960
;
; diff[e; x] differentiates expression e with respect to x
; M-expression form (from the paper):
;   diff[e; x] = [atom[e] -> [eq[e; x] -> 1; T -> 0];
;                 eq[car[e]; PLUS] -> list[PLUS; diff[cadr[e]; x]; diff[caddr[e]; x]];
;                 eq[car[e]; TIMES] -> list[PLUS;
;                     list[TIMES; cadr[e]; diff[caddr[e]; x]];
;                     list[TIMES; diff[cadr[e]; x]; caddr[e]]];
;                 T -> UNDEFINED]

((LABEL DIFF
  (LAMBDA (E X)
    (COND
      ((ATOM E)
       (COND ((EQ E X) (QUOTE 1))
             (T (QUOTE 0))))
      ((EQ (CAR E) (QUOTE PLUS))
       (LIST (QUOTE PLUS)
             (DIFF (CADR E) X)
             (DIFF (CADDR E) X)))
      ((EQ (CAR E) (QUOTE TIMES))
       (LIST (QUOTE PLUS)
             (LIST (QUOTE TIMES) (CADR E) (DIFF (CADDR E) X))
             (LIST (QUOTE TIMES) (DIFF (CADR E) X) (CADDR E))))
      (T (QUOTE UNDEFINED)))))
 (QUOTE (PLUS (TIMES X X) X))
 (QUOTE X))
