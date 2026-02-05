# Fibonacci sequence calculator
def fibonacci(n)
    if n <= 1
        return n
    end
    return fibonacci(n - 1) + fibonacci(n - 2)
end

# Print first 10 Fibonacci numbers
for i : 0..9
    print("F(" + str(i) + ") = " + str(fibonacci(i)))
end
