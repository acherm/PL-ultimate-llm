queens(N, Queens) :-
    length(Queens, N),
    Queens :: 1..N,
    all_different(Queens),
    safe(Queens).

safe([]).
safe([Queen|Queens]) :-
    safe(Queens, Queen, 1),
    safe(Queens).

safe([], _, _).
safe([Queen|Queens], Queen0, Dist) :-
    Queen0 + Dist #\= Queen,
    Queen0 - Dist #\= Queen,
    Dist1 is Dist + 1,
    safe(Queens, Queen0, Dist1).
