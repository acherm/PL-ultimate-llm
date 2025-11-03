package Adder

with SPARK_Mode,
     Abstract_State => (State with External => Async_Readers,
                               Part_Of  => References.States)

is

   procedure Add (X, Y : Integer; Result : out Integer)
   with Global => null,
        Depends => (Result => (X, Y)),
        Pre     => X'Valid and Y'Valid and
                   X <= Integer'Last - Y,
        Post    => Result'Valid and Result = X + Y;

end Adder;