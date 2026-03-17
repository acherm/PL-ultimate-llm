begin
  comment Compute sum of integers 1 to 10 in SMALGOL;
  integer i, sum;
  sum := 0;
  for i := 1 step 1 until 10 do
    sum := sum + i;
  print(sum)
end