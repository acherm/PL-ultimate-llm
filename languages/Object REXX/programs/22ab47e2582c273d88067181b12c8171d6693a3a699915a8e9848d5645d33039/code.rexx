/* Fibonacci sequence in Object REXX (ooRexx) */
do i = 0 to 10
  say 'fib('i') =' fib(i)
end
exit

fib: procedure
  use arg n
  if n <= 1 then return n
  return fib(n-1) + fib(n-2)
