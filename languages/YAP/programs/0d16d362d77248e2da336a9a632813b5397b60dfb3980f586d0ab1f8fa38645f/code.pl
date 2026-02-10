% Factorial implementation in YAP Prolog
% From YAP documentation examples

factorial(0, 1) :- !.
factorial(N, F) :-
    N > 0,
    N1 is N - 1,
    factorial(N1, F1),
    F is N * F1.

% Query examples:
% ?- factorial(5, X).
% X = 120
%
% ?- factorial(10, X).
% X = 3628800