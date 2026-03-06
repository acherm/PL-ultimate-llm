/* Fibonacci sequence using Object REXX classes */

::class FibSolver public

::method init
  expose memo
  memo = .Directory~new

::method solve
  expose memo
  use arg n
  if n <= 1 then return n
  cached = memo[n]
  if cached \= .nil then return cached
  result = self~solve(n-1) + self~solve(n-2)
  memo[n] = result
  return result

-- Main program
solver = .FibSolver~new
say 'Fibonacci sequence (memoized):'
do i = 0 to 10
  say '  fib('||i||') =' solver~solve(i)
end
