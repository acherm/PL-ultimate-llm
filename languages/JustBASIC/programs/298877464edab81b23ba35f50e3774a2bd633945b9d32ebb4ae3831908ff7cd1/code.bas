dim fib(10)
fib(1) = 1
fib(2) = 1
for n = 3 to 10
    fib(n) = fib(n-1) + fib(n-2)
next n
for n = 1 to 10
    print n; ": "; fib(n)
next n
end
