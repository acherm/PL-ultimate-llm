% List operations in Tau Prolog

% append/3 - concatenate two lists
append([], L, L).
append([H|T], L, [H|R]) :- append(T, L, R).

% length/2 - find the length of a list
length([], 0).
length([_|T], N) :- length(T, N1), N is N1 + 1.

% member/2 - check if element is in list
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

% reverse/2 - reverse a list
reverse([], []).
reverse([H|T], R) :- reverse(T, RT), append(RT, [H], R).
