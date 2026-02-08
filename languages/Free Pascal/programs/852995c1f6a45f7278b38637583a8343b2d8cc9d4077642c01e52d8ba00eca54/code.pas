program Fibonacci;

var
  n, i: Integer;
  fib, prev, temp: Int64;

begin
  Write('Enter the number of Fibonacci terms: ');
  ReadLn(n);

  if n <= 0 then
  begin
    WriteLn('Please enter a positive integer.');
    Exit;
  end;

  prev := 0;
  fib := 1;

  WriteLn('Fibonacci sequence:');

  for i := 1 to n do
  begin
    WriteLn(i, ': ', prev);
    temp := fib;
    fib := prev + fib;
    prev := temp;
  end;
end.