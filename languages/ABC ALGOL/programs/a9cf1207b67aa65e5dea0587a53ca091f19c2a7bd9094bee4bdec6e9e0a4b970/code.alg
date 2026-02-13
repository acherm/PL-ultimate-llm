begin
   integer procedure fibonacci(n);
      integer n;
   begin
      integer a, b, temp, i;
      a := 0;
      b := 1;
      if n = 0 then fibonacci := 0
      else if n = 1 then fibonacci := 1
      else begin
         for i := 2 step 1 until n do
         begin
            temp := a + b;
            a := b;
            b := temp
         end;
         fibonacci := b
      end
   end;

   integer k;
   for k := 0 step 1 until 10 do
      outinteger(1, fibonacci(k))
end