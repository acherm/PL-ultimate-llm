begin
   integer procedure factorial(n);
      value n; integer n;
   begin
      if n = 0 then factorial := 1
      else factorial := n * factorial(n - 1)
   end;

   integer i;
   for i := 0 step 1 until 10 do
      print(i, factorial(i))
end
