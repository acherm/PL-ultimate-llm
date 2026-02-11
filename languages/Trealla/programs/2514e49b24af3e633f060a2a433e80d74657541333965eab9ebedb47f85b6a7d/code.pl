% List membership check
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

% List append
append([], L, L).
append([H|T], L, [H|R]) :- append(T, L, R).

% List length
length([], 0).
length([_|T], N) :- length(T, N1), N is N1 + 1.

% Factorial
factorial(0, 1).
factorial(N, F) :- N > 0, N1 is N - 1, factorial(N1, F1), F is N * F1.
