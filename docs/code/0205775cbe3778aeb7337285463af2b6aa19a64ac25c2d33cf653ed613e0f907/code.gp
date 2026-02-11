\ Compute the n'th Fibonacci number
fib(n) = if(n < 2, n, fib(n-1) + fib(n-2));
for(n = 0, 9,
  write("fibonacci(" n ") = " fib(n));
)