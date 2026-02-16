% List manipulation examples in Ichiban Prolog

% Append two lists
append([], L, L).
append([H|T], L, [H|R]) :- append(T, L, R).

% Length of a list
length([], 0).
length([_|T], N) :- length(T, N1), N is N1 + 1.

% Reverse a list
reverse([], []).
reverse([H|T], R) :- reverse(T, RT), append(RT, [H], R).

% Member check
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

% Last element of a list
last([X], X).
last([_|T], X) :- last(T, X).

% Examples
:- initialization(main).

main :-
    % Test append
    append([1, 2], [3, 4], L1),
    write('Append [1,2] and [3,4]: '), write(L1), nl,

    % Test length
    length([a, b, c, d], Len),
    write('Length of [a,b,c,d]: '), write(Len), nl,

    % Test reverse
    reverse([1, 2, 3, 4], L2),
    write('Reverse [1,2,3,4]: '), write(L2), nl,

    % Test member
    (member(3, [1, 2, 3, 4]) -> write('3 is member of [1,2,3,4]') ; write('3 is not member')), nl,

    % Test last
    last([a, b, c], Last),
    write('Last of [a,b,c]: '), write(Last), nl,

    halt.