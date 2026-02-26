program mutual;

var
  shared: integer;

process one;
var
  loop: integer;
begin
  for loop := 1 to 20 do
    shared := shared + 1
end;

process two;
var
  loop: integer;
begin
  for loop := 1 to 20 do
    shared := shared + 1
end;

begin
  shared := 0;
  cobegin
    one;
    two
  coend;
  writeln(shared)
end.
