:- module(quicksort, [qsort/2]).

qsort([], []).
qsort([H|T], Sorted) :-
    partition(H, T, Left, Right),
    qsort(Left, SortedLeft),
    qsort(Right, SortedRight),
    append(SortedLeft, [H|SortedRight], Sorted).

partition(_, [], [], []).
partition(Pivot, [H|T], [H|Left], Right) :-
    H =< Pivot, !,
    partition(Pivot, T, Left, Right).
partition(Pivot, [H|T], Left, [H|Right]) :-
    H > Pivot,
    partition(Pivot, T, Left, Right).

:- initialization(main, main).
main :-
    qsort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], Sorted),
    write(Sorted), nl.
