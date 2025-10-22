parent(john, mary).
parent(john, tom).
parent(mary, alice).
parent(tom, bob).

sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.

% Example Queries:
% ?- sibling(alice, bob).
% ?- sibling(mary, tom).