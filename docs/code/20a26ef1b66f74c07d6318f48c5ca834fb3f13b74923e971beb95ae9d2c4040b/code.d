proc main() void:
    int n;

    writeln("Enter a number:");
    readln(n);
    writeln("Fibonacci(", n, ") = ", fib(n))
corp

proc fib(int n) int:
    if n <= 1 then
        n
    else
        fib(n-1) + fib(n-2)
    fi
corp