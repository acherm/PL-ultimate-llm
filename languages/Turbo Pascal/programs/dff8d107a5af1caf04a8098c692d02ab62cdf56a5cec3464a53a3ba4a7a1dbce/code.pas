program SieveOfEratosthenes;
uses Crt;

const
  MaxNum = 100;

var
  IsPrime: array[2..MaxNum] of Boolean;
  I, J: Integer;

begin
  ClrScr;
  
  { Initialize all numbers as prime }
  for I := 2 to MaxNum do
    IsPrime[I] := True;
  
  { Sieve of Eratosthenes }
  for I := 2 to Trunc(Sqrt(MaxNum)) do
  begin
    if IsPrime[I] then
    begin
      J := I * I;
      while J <= MaxNum do
      begin
        IsPrime[J] := False;
        J := J + I;
      end;
    end;
  end;
  
  { Print all prime numbers }
  WriteLn('Prime numbers from 2 to ', MaxNum, ':');
  WriteLn;
  for I := 2 to MaxNum do
  begin
    if IsPrime[I] then
      Write(I:4);
  end;
  WriteLn;
  WriteLn;
  WriteLn('Press any key to continue...');
  ReadKey;
end.
