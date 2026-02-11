begin
   comment GIER ALGOL example - compute factorial;
   integer n, fact;
   
   procedure factorial(n, result);
      value n;
      integer n, result;
   begin
      integer i, temp;
      temp := 1;
      for i := 1 step 1 until n do
         temp := temp * i;
      result := temp
   end factorial;
   
   n := 5;
   factorial(n, fact);
   outinteger(1, fact)
end
