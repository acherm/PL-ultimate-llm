program pascal_triangle;

procedure print_triangle(n: integer);
var
  i, j: integer;
  a: array of array of integer;
begin
  setlength(a, n, n);
  for i := 0 to n - 1 do
  begin
    for j := 0 to i do
    begin
      if (j = 0) or (j = i) then
        a[i, j] := 1
      else
        a[i, j] := a[i - 1, j - 1] + a[i - 1, j];
      write(a[i, j], ' ');
    end;
    writeln;
  end;
end;

begin
  print_triangle(10);
end.