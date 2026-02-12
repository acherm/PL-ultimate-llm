/ Fibonacci sequence generator in q
fib:{$[x<2;x;.z.s[x-1]+.z.s[x-2]]}
/ Generate first 10 Fibonacci numbers
fib each til 10
