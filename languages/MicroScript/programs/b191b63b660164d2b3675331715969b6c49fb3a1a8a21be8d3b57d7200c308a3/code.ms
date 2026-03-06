// Fibonacci sequence in MicroScript

fibonacci = function(n)
  if n <= 0 then return 0 end
  if n == 1 then return 1 end
  a = 0
  b = 1
  for i = 2 to n
    c = a + b
    a = b
    b = c
  end
  return b
end

for i = 0 to 9
  print("fib(" + i + ") = " + fibonacci(i))
end
