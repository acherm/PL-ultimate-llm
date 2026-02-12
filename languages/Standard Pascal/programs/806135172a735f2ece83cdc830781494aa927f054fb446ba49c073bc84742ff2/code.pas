program Sieve;
const
  MAX = 100;
var
  prime: array [2..MAX] of boolean;
  i, j: integer;
begin
  for i := 2 to MAX do
    prime[i] := true;

  for i := 2 to MAX do
  begin
    if prime[i] then
    begin
      writeln(i);
      j := i * 2;
      while j <= MAX do
      begin
        prime[j] := false;
        j := j + i
      end
    end
  end
end.