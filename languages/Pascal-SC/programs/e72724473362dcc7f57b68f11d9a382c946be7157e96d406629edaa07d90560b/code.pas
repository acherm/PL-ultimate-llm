program Factorial;
{ This program computes the factorial of a number }

var
  n, i: integer;
  result: real;

begin
  write('Enter a number: ');
  readln(n);
  
  result := 1.0;
  for i := 1 to n do
    result := result * i;
  
  writeln('Factorial of ', n, ' is ', result:0:0);
end.
