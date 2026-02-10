% Hamiltonian Cycle Problem
% Generate: select edges
{ in_path(X,Y) : edge(X,Y) } = 1 :- node(X).
{ in_path(X,Y) : edge(X,Y) } = 1 :- node(Y).

% Define: path connectivity
reached(X) :- start(X).
reached(Y) :- reached(X), in_path(X,Y).

% Test: all nodes must be reached
:- node(X), not reached(X).

% Example graph
node(1..4).
edge(1,2). edge(2,3). edge(3,4). edge(4,1).
edge(1,3). edge(2,4).
start(1).

#show in_path/2.
