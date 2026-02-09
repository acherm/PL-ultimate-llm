program Fibonacci;

var n, i: integer;
    a, b, temp: int64;

begin
  n := 20;
  a := 0;
  b := 1;
  writeln('Fibonacci sequence (first ', n, ' terms):');
  for i := 1 to n do
  begin
    write(a, ' ');
    temp := a + b;
    a := b;
    b := temp;
  end;
  writeln;
  writeln('Done.');
end.
