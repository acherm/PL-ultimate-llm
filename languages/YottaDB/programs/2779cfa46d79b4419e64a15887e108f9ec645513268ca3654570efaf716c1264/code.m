fib(n)
    ; Calculate nth Fibonacci number
    if n<=1 quit n
    quit $$fib(n-1)+$$fib(n-2)

main
    new i
    write "Fibonacci sequence:",!
    for i=0:1:10 do
    . write i,": ",$$fib(i),!
    quit
