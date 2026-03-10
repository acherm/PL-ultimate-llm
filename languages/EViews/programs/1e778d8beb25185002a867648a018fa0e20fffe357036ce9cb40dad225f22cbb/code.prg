' Fibonacci sequence in EViews
' Demonstrates vector operations and looping constructs

vector(10) fib

fib(1) = 1
fib(2) = 1

for !i = 3 to 10
    fib(!i) = fib(!i-1) + fib(!i-2)
next

' Display the results
for !j = 1 to 10
    @disp "Fib(" + @str(!j) + ") = " + @str(fib(!j))
next
