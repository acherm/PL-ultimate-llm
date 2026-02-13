program Factorial;
{ Calculates factorial of a number }

var
  n, i: Integer;
  result: LongInt;

begin
  Write('Enter a number: ');
  ReadLn(n);

  result := 1;
  for i := 2 to n do
    result := result * i;

  WriteLn('Factorial of ', n, ' is ', result);
end.