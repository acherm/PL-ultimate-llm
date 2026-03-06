module lists.

kind list   type -> type.
type nil    list A.
type cons   A -> list A -> list A.

type append  list A -> list A -> list A -> o.
type length  list A -> int -> o.
type member  A -> list A -> o.
type reverse  list A -> list A -> o.
type rev_aux  list A -> list A -> list A -> o.

append nil L L.
append (cons X L1) L2 (cons X L3) :- append L1 L2 L3.

length nil 0.
length (cons _ L) N :- length L M, N is M + 1.

member X (cons X _).
member X (cons _ L) :- member X L.

rev_aux nil Acc Acc.
rev_aux (cons X L) Acc Result :- rev_aux L (cons X Acc) Result.

reverse L R :- rev_aux L nil R.
