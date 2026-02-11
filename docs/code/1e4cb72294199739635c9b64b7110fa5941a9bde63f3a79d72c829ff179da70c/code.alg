begin
  integer procedure factorial(n);
  value n;
  integer n;
  begin
    integer result;
    result := 1;
    for i := 1 step 1 until n do
      result := result * i;
    factorial := result
  end;

  integer n;
  n := 5;
  print(factorial(n))
end
