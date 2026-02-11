-- Factorial function with Ravi type annotations
function factorial(n: integer): integer
  if n <= 1 then
    return 1
  else
    return n * factorial(n - 1)
  end
end

-- Test the function
for i = 1, 10 do
  print(string.format("factorial(%d) = %d", i, factorial(i)))
end
