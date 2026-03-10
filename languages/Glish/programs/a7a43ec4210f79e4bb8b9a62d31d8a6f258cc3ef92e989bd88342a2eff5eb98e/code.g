# Fibonacci sequence in Glish
# Demonstrates functions, loops, and vectors

func fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

# Build a record with results
results := [=];
for (i := 0; i <= 9; i +:= 1) {
    results[i+1] := fibonacci(i);
}

print("First 10 Fibonacci numbers:");
print(results);

# Vector sum using built-in
v := [1, 1, 2, 3, 5, 8, 13, 21, 34, 55];
print("Sum of first 10 Fibonacci numbers:", sum(v));
