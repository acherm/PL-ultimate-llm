/* Factorial calculator in REXX */
say "Enter a number:"
pull num
if datatype(num,'W') & num >= 0 then do
  result = factorial(num)
  say num"! =" result
end
else
  say "Please enter a non-negative integer"
exit

factorial: procedure
  arg n
  if n = 0 | n = 1 then
    return 1
  else
    return n * factorial(n-1)
