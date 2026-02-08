# Fibonacci function in Nasal
var fibonacci = func(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

# Calculate and print first 10 Fibonacci numbers
for (var i = 0; i < 10; i += 1) {
    print("fibonacci(", i, ") = ", fibonacci(i));
}