module nat.

kind nat type.

type z nat.
type s nat -> nat.

type plus nat -> nat -> nat -> o.

plus z N N.
plus (s M) N (s P) :- plus M N P.

type times nat -> nat -> nat -> o.

times z N z.
times (s M) N P :- times M N Q, plus Q N P.
