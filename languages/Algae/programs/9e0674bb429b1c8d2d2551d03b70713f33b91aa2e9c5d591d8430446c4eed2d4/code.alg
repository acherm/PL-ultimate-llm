#!/usr/bin/algae

# Fibonacci sequence calculator
fib := function(n) {
    if (n <= 1) {
        return n;
    } else {
        return fib(n - 1) + fib(n - 2);
    }
};

# Print first 15 Fibonacci numbers
for (i := 0; i < 15; i := i + 1) {
    println(fib(i));
}
