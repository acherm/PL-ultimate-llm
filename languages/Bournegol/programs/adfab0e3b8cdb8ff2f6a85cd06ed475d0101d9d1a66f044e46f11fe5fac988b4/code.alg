begin
  integer i, sum;
  sum := 0;
  for i := 1 step 1 until 10 do
    sum := sum + i;
  outstring(1, "Sum of 1 to 10 is: ");
  outinteger(1, sum);
  outstring(1, "\n")
end
