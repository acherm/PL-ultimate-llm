/* Factorial calculation in Turbo Prolog */

domains
  number = integer

predicates
  factorial(number, number)
  run

clauses
  factorial(0, 1).
  factorial(N, F) :-
    N > 0,
    N1 = N - 1,
    factorial(N1, F1),
    F = N * F1.

  run :-
    factorial(5, Result),
    write("Factorial of 5 is: "), write(Result), nl.

goal
  run.