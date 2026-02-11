routine factorial(n: integer) returns integer
  pre n >= 0
  post result = if n = 0 then 1 else n * factorial(n-1)
begin
  var result: integer;

  if n = 0 then
    result := 1
  else
    result := n * factorial(n - 1);

  return result
end factorial;
