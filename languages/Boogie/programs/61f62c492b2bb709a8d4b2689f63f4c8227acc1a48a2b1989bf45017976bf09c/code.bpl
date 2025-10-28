// Simple example: Zeroing the first array element

function Sum(A: [int]int, B: int, E: int) returns (s: int)
  requires B <= E;
  ensures s == (if B == E then 0 else A[B] + Sum(A, B+1, E));
{
  if (B == E) then 0 else A[B] + Sum(A, B+1, E)
}

procedure ZeroFirst(A: [int]int, m: int, n: int) returns (A': [int]int)
  requires 0 <= m && m < n;
  requires (forall i: int :: 0 <= i && i < n ==> A[i] >= 0);
  ensures (forall i: int :: 0 <= i && i < n ==> A'[i] == if i == 0 then 0 else A[i]);
  ensures Sum(A', 0, n) == Sum(A, 1, n);
{
  A' := A[0 := 0];
}