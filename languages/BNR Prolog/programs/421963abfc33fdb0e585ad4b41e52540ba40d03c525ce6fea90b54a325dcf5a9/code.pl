% BNR Prolog example: Interval arithmetic constraint solving
% Solving a system with interval constraints

:- use_module(library(clpBNR)).

% Define a predicate to solve for X and Y given constraints
solve_intervals(X, Y) :-
    X:: 0..10,
    Y:: 0..10,
    {X + Y == 10},
    {X * Y >= 20},
    {X >= Y}.

% Example query to find solutions
% ?- solve_intervals(X, Y).
