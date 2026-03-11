program fibonacci;
var
  i    : integer;
  prev2, prev1, current : longint;
begin
  prev2 := 0;
  prev1 := 1;
  writeln(prev2);
  writeln(prev1);
  for i := 1 to 18 do begin
    current := prev1 + prev2;
    write(current);
    writeln;
    prev2 := prev1;
    prev1 := current
  end
end.
