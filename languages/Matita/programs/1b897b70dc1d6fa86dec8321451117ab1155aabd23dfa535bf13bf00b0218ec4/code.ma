include "basics/pts.ma".

inductive nat : Type[0] ≝
  | O : nat
  | S : nat → nat.

let rec plus n m on n ≝
  match n with
  [ O ⇒ m
  | S p ⇒ S (plus p m)
  ].

let rec times n m on n ≝
  match n with
  [ O ⇒ O
  | S p ⇒ plus m (times p m)
  ].

theorem plus_O_n : ∀n:nat. plus O n = n.
#n normalize //
qed.

theorem plus_n_O : ∀n:nat. plus n O = n.
#n elim n
  [ normalize //
  | #p #IH normalize >IH //
  ]
qed.

theorem plus_n_Sm : ∀n,m:nat. S (plus n m) = plus n (S m).
#n #m elim n
  [ normalize //
  | #p #IH normalize >IH //
  ]
qed.

theorem plus_comm : ∀n,m:nat. plus n m = plus m n.
#n #m elim n
  [ normalize >(plus_n_O m) //
  | #p #IH normalize >IH >(plus_n_Sm m p) //
  ]
qed.
