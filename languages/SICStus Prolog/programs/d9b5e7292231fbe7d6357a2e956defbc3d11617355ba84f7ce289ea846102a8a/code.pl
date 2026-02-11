% Quicksort implementation in Prolog
quicksort([], []).
quicksort([H|T], Sorted) :-
    partition(H, T, Left, Right),
    quicksort(Left, SortedLeft),
    quicksort(Right, SortedRight),
    append(SortedLeft, [H|SortedRight], Sorted).

partition(_, [], [], []).
partition(Pivot, [H|T], [H|Left], Right) :-
    H =< Pivot,
    partition(Pivot, T, Left, Right).
partition(Pivot, [H|T], Left, [H|Right]) :-
    H > Pivot,
    partition(Pivot, T, Left, Right).
