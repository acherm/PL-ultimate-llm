% FOIL program to learn family relationships
% Background knowledge
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).
parent(pat, jim).

male(tom).
male(bob).
male(jim).
female(liz).
female(ann).
female(pat).

% Target relation to learn
father(X, Y) :- parent(X, Y), male(X).
mother(X, Y) :- parent(X, Y), female(X).
grandfather(X, Z) :- father(X, Y), parent(Y, Z).
