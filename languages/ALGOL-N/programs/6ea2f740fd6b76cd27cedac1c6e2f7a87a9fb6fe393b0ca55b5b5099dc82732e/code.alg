begin
   integer procedure factorial(n);
   value n;
   integer n;
   begin
      integer result;
      result := 1;
      for i := 2 step 1 until n do
         result := result * i;
      factorial := result
   end;

   integer i;
   for i := 1 step 1 until 10 do
      print(i, factorial(i))
end