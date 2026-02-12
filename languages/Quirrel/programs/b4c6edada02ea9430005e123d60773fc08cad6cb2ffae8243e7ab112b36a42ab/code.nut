// Fibonacci sequence calculator
function fibonacci(n) {
  if (n <= 1)
    return n
  return fibonacci(n - 1) + fibonacci(n - 2)
}

// Print first 10 Fibonacci numbers
for (local i = 0; i < 10; i++) {
  print("fib(" + i + ") = " + fibonacci(i) + "\n")
}
