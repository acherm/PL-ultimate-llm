Require Import Ynot.

Open Local Scope hprop_scope.
Open Local Scope stsepi_scope.

(* Swap two heap cells using separation logic *)
Definition swap (x y : ptr) :
  STsep (fun h => Exists vx :@ nat, Exists vy :@ nat,
                  x --> vx * y --> vy)
        (fun _ _ h => Exists vx :@ nat, Exists vy :@ nat,
                      x --> vy * y --> vx) :=
  vx <- !x;
  vy <- !y;
  x ::= vy;;
  y ::= vx;;
  Return tt.
