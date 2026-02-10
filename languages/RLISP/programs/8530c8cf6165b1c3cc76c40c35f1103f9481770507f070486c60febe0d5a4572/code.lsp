% Factorial function in RLISP
procedure factorial(n);
   if n = 0 then 1
   else n * factorial(n - 1);

% Fibonacci function in RLISP
procedure fibonacci(n);
   if n <= 1 then n
   else fibonacci(n - 1) + fibonacci(n - 2);

% GCD function in RLISP
procedure gcd(a, b);
   if b = 0 then a
   else gcd(b, remainder(a, b));

% List length function in RLISP
procedure length(lst);
   if null lst then 0
   else 1 + length(cdr lst);

% List reverse function in RLISP
procedure reverse(lst);
   reverse1(lst, nil);

procedure reverse1(lst, acc);
   if null lst then acc
   else reverse1(cdr lst, car lst . acc);
