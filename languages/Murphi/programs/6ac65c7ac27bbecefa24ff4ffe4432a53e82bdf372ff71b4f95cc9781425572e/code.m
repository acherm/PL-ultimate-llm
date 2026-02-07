-- Simple mutual exclusion protocol
const
  N: 2;  -- number of processes

type
  pid: 0..N-1;

var
  flag: array [pid] of boolean;
  turn: pid;
  critical: array [pid] of boolean;

ruleset i: pid do
  rule "Request entry"
    !flag[i]
  ==>
  begin
    flag[i] := true;
    turn := i;
  end;

  rule "Enter critical section"
    flag[i] & forall j: pid do (j = i | !flag[j] | turn = i) end
  ==>
  begin
    critical[i] := true;
  end;

  rule "Exit critical section"
    critical[i]
  ==>
  begin
    critical[i] := false;
    flag[i] := false;
  end;
end;

startstate
  for i: pid do
    flag[i] := false;
    critical[i] := false;
  end;
  turn := 0;
end;

invariant "Mutual exclusion"
  forall i: pid do
    forall j: pid do
      (i != j) -> !(critical[i] & critical[j])
    end
  end;