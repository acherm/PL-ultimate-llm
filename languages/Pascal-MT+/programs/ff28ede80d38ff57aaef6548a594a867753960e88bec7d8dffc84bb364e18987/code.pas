program Fibonacci;

var
  n    : integer;
  a, b : integer;
  temp : integer;

begin
  writeln('First 20 Fibonacci numbers:');
  a := 0;
  b := 1;
  for n := 1 to 20 do
  begin
    writeln(n:3, ': ', a:6);
    temp := a + b;
    a    := b;
    b    := temp;
  end;
end.