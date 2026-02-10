% N-Queens problem in B-Prolog
queens(N, Qs) :-
    length(Qs, N),
    Qs :: 1..N,
    all_different(Qs),
    safe(Qs),
    labeling(Qs).

safe([]).
safe([Q|Qs]) :-
    safe(Qs, Q, 1),
    safe(Qs).

safe([], _, _).
safe([Q|Qs], Q0, D) :-
    Q0 #\= Q + D,
    Q0 #\= Q - D,
    D1 is D + 1,
    safe(Qs, Q0, D1).

go :- queens(8, Qs), writeln(Qs).
