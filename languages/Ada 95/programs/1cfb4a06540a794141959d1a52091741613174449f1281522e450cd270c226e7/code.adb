with Ada.Text_IO; use Ada.Text_IO;

procedure Fibonacci is
   function Fib (N : Natural) return Natural is
   begin
      if N <= 1 then
         return N;
      else
         return Fib (N - 1) + Fib (N - 2);
      end if;
   end Fib;

begin
   for I in 0 .. 10 loop
      Put_Line (Natural'Image (Fib (I)));
   end loop;
end Fibonacci;
