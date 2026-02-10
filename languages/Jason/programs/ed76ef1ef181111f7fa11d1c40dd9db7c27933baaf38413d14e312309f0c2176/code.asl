// Jason agent that computes Fibonacci numbers
// Based on AgentSpeak(L) semantics

/* Initial beliefs */
fib(0, 0).
fib(1, 1).

/* Plans */
+!compute_fib(N) : N > 1 <-
    N1 = N - 1;
    N2 = N - 2;
    !compute_fib(N1);
    !compute_fib(N2);
    ?fib(N1, F1);
    ?fib(N2, F2);
    F = F1 + F2;
    +fib(N, F);
    .print("fib(", N, ") = ", F).

+!compute_fib(N) : N <= 1 <-
    ?fib(N, F);
    .print("fib(", N, ") = ", F).

/* Initial goal */
!compute_fib(10).