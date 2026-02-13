# Fibonacci sequence calculator
fib = n =>
  if n <= 1
    n
  else
    fib(n - 1) + fib(n - 2)

# Calculate first 10 Fibonacci numbers
main = do
  for i in range(10):
    print(fib(i))
