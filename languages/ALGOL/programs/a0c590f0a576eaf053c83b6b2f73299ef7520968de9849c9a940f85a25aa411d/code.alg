real procedure det(A, n); value n; array A; integer n;
begin
    integer i, j, k;
    real d;
    boolean procedure even(k); value k; integer k;
        even := k = 2 × (k ÷ 2);
    d := 1;
    for k := 1 step 1 until n - 1 do
    begin
        for i := k + 1 step 1 until n do
        begin
            for j := k + 1 step 1 until n do
                A[i,j] := A[i,j] - A[i,k] × A[k,j] / A[k,k];
            A[i,k] := 0
        end
    end;
    for k := 1 step 1 until n do d := d × A[k,k];
    det := if even(n) then d else -d
end