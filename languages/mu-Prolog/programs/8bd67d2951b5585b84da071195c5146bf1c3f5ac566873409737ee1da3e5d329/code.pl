qsort([], []).
qsort([H|T], Sorted) :-
    partition(H, T, Less, Greater),
    qsort(Less, SortedLess),
    qsort(Greater, SortedGreater),
    append(SortedLess, [H|SortedGreater], Sorted).

partition(_, [], [], []).
partition(Pivot, [H|T], [H|Less], Greater) :-
    H =< Pivot, !,
    partition(Pivot, T, Less, Greater).
partition(Pivot, [H|T], Less, [H|Greater]) :-
    partition(Pivot, T, Less, Greater).

append([], L, L).
append([H|T], L, [H|R]) :- append(T, L, R).

:- qsort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3], S), write(S), nl.
