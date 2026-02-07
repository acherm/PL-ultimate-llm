module append_example.

% Type declarations
type list A -> type.
type nil list A.
type cons A -> list A -> list A.
type append list A -> list A -> list A -> o.

% Append predicate definition
append nil L L.
append (cons X L1) L2 (cons X L3) :- append L1 L2 L3.

% Example query (commented)
% ?- append (cons 1 (cons 2 nil)) (cons 3 nil) L.
% L = cons 1 (cons 2 (cons 3 nil))
