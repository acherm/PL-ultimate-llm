display { for n = 0 to 9 do fib(n) }

where

  fib(0) = 0;
  fib(1) = 1;
  fib(n) = fib(n-1) + fib(n-2) if n > 1 else 0;