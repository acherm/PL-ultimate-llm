// Fibonacci sequence in MiniScript
fibonacci = function(n)
    if n <= 1 then return n
    return fibonacci(n - 1) + fibonacci(n - 2)
end function

// Print first 10 Fibonacci numbers
for i in range(0, 9)
    print "fibonacci(" + i + ") = " + fibonacci(i)
end for
