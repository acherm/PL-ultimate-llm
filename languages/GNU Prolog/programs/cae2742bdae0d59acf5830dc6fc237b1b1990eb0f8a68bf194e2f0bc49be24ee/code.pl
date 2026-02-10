:- initialization(main).

queens(N, Qs) :-
    length(Qs, N),
    fd_domain(Qs, 1, N),
    safe(Qs),
    fd_labeling(Qs).

safe([]).
safe([Q|Qs]) :-
    no_attack(Q, Qs, 1),
    safe(Qs).

no_attack(_, [], _).
no_attack(Q, [Q1|Qs], D) :-
    Q #\= Q1,
    Q #\= Q1 + D,
    Q #\= Q1 - D,
    D1 is D + 1,
    no_attack(Q, Qs, D1).

main :-
    queens(8, Qs),
    write(Qs), nl,
    halt.
