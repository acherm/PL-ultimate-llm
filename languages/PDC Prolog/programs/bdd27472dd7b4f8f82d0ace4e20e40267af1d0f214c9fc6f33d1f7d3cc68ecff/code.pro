/* Maximum element in a list - PDC Prolog */
domains
  numlist = integer*
  num = integer

predicates
  max_list(numlist, num)
  max_of(num, num, num)

clauses
  max_of(X, Y, X) :- X >= Y, !.
  max_of(_, Y, Y).

  max_list([H], H) :- !.
  max_list([H|T], Max) :-
    max_list(T, TMax),
    max_of(H, TMax, Max).

goal
  max_list([3, 1, 4, 1, 5, 9, 2, 6, 5, 3], Max),
  write("Maximum: "), write(Max), nl.
