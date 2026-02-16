// Fibonacci sequence generator
let fibonacci(n) =
  if n <= 1
    n
  else
    fibonacci(n - 1) + fibonacci(n - 2)

for i in 0 to 10
  console.log "fibonacci(\(i)) = \(fibonacci(i))"
