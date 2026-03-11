program Sieve;
const nmax = 100;
var p: array[2..nmax] of boolean;
    i, j: integer;
begin
  for i := 2 to nmax do
    p[i] := true;
  for i := 2 to nmax do
    if p[i] then begin
      j := 2*i;
      while j <= nmax do begin
        p[j] := false;
        j := j+i
      end;
      write(i, ' ')
    end;
  writeln
end.