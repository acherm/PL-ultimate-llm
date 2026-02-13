proc fibonacci(n: int): int =
  if n < 2:
    return n
  else:
    return fibonacci(n - 1) + fibonacci(n - 2)

for i in 0..10:
  echo "fibonacci(", i, ") = ", fibonacci(i)
