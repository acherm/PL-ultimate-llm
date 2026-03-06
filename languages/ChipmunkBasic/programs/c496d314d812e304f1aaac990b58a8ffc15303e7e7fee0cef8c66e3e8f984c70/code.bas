' Fibonacci sequence in Chipmunk Basic
dim fib(20)
fib(0) = 0
fib(1) = 1
for i = 2 to 19
    fib(i) = fib(i-1) + fib(i-2)
next i
for i = 0 to 19
    print fib(i)
next i
end