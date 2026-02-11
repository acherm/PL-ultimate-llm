program Fibonacci;

{$APPTYPE CONSOLE}

uses
  SysUtils;

function Fib(n: Integer): Int64;
begin
  if n <= 1 then
    Result := n
  else
    Result := Fib(n - 1) + Fib(n - 2);
end;

var
  i: Integer;
begin
  WriteLn('Fibonacci sequence:');
  for i := 0 to 10 do
    WriteLn('Fib(', i, ') = ', Fib(i));
  ReadLn;
end.
