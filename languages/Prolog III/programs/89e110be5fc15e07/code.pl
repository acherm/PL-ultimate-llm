% Simple constraint example in Prolog III
% Define a relation with constraints
range(X, Y, Z) :-
    X < Y,
    Y < Z,
    X + Y + Z = 15.

% Query to find values
?- range(A, B, C), A > 1, C < 10.
