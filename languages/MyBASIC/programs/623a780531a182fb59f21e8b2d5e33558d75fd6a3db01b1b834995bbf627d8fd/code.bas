' Fibonacci numbers in MY-BASIC
def fib(n)
  if n <= 1 then
    return n
  end if
  return fib(n - 1) + fib(n - 2)
end def

dim i as integer
for i = 0 to 10
  print fib(i); " ";
next i
print
