% Fibonacci sequence in Erlog (Prolog interpreter for Erlang)
% Classic recursive definition

fib(0, 0).
fib(1, 1).
fib(N, F) :-
    N > 1,
    N1 is N - 1,
    N2 is N - 2,
    fib(N1, F1),
    fib(N2, F2),
    F is F1 + F2.

% Collect first N+1 fibonacci numbers into a list
fib_list(0, [F]) :- fib(0, F).
fib_list(N, Fibs) :-
    N > 0,
    N1 is N - 1,
    fib_list(N1, Rest),
    fib(N, F),
    append(Rest, [F], Fibs).

% Entry point: print fibs from 0 to 10
:- fib_list(10, Fibs),
   write(Fibs), nl.
