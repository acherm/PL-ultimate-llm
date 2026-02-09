% Probabilistic graph reachability in ProbLog
% Each edge exists with a certain probability

0.6::edge(1,2).
0.1::edge(1,3).
0.4::edge(2,5).
0.3::edge(2,6).
0.3::edge(3,4).
0.8::edge(4,5).
0.2::edge(5,6).

% Path definition (deterministic rules)
path(X,Y) :- edge(X,Y).
path(X,Y) :- edge(X,Z), path(Z,Y).

% Queries: what is the probability of reaching node 5 or 6 from node 1?
query(path(1,5)).
query(path(1,6)).
