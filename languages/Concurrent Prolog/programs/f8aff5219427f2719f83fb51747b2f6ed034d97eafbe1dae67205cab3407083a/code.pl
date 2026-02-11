merge([], L, L).
merge(L, [], L).
merge([X|Xs], [Y|Ys], [X|Zs]) :- X =< Y, merge(Xs, [Y|Ys], Zs).
merge([X|Xs], [Y|Ys], [Y|Zs]) :- X > Y, merge([X|Xs], Ys, Zs).

split([], [], []).
split([X], [X], []).
split([X,Y|Zs], [X|Xs], [Y|Ys]) :- split(Zs, Xs, Ys).

mergesort([], []).
mergesort([X], [X]).
mergesort(L, SL) :-
    split(L, L1, L2),
    mergesort(L1, SL1),
    mergesort(L2, SL2),
    merge(SL1, SL2, SL).