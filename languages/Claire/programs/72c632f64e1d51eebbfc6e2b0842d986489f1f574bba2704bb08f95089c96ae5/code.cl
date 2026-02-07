// Factorial function in Claire
factorial(n:integer) : integer
 -> (if (n <= 1) 1
     else n * factorial(n - 1))

// Test
main() -> (printf("Factorial of 5 is ~S~%", factorial(5)))
