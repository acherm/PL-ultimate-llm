program Factorial;

var
  n, i: integer;
  result: integer;

function Fact(num: integer): integer;
var
  i, f: integer;
begin
  f := 1;
  for i := 2 to num do
    f := f * i;
  Fact := f
end;

begin
  writeln('Factorial Calculator');
  writeln('====================');
  for n := 0 to 12 do
  begin
    result := Fact(n);
    writeln(n:3, '! = ', result:10)
  end
end.
