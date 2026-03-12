module lists.

type app   list A -> list A -> list A -> o.
type rev   list A -> list A -> o.

app nil L L.
app (X :: L1) L2 (X :: L3) :- app L1 L2 L3.

rev nil nil.
rev (X :: L) R :- rev L RL, app RL (X :: nil) R.
