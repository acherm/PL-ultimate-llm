% N-Prolog example: Hypothetical implications
% Gabbay & Reyle, Journal of Logic Programming, 1984

parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).

ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

% Hypothetical query: under the assumption that ann is parent of carol,
% is tom an ancestor of carol?
:- ( parent(ann, carol) => ancestor(tom, carol) ),
   write(yes), nl.
