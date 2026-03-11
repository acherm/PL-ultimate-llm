# Fibonacci sequence in NFun
fib(n:int):int = if(n <= 1) n else fib(n-1) + fib(n-2)

# Compute first 10 fibonacci numbers
result:int[] = [0..9].map(rule fib(it))
out = result