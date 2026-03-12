(* Sieve of Eratosthenes - ORCA/Pascal *)
program Sieve;

const
  Max = 100;

var
  flags: array[2..Max] of boolean;
  i, j, count: integer;

begin
  for i := 2 to Max do
    flags[i] := true;

  count := 0;
  for i := 2 to Max do
  begin
    if flags[i] then
    begin
      count := count + 1;
      j := i + i;
      while j <= Max do
      begin
        flags[j] := false;
        j := j + i
      end
    end
  end;

  writeln('Primes up to ', Max, ': ', count)
end.
